from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from borg_descriptor_threadsafe import ApplicationConfig, ThreadSafeSharedAttribute
import threading


class ThreadSafeBorgDescriptorTestCase(TestCase):

    def setUp(self):
        # Reset descriptor values before each test
        ApplicationConfig.db_url._value = "sqlite:///default.db"
        ApplicationConfig.debug._value = False
        ApplicationConfig.pool_size._value = 5
        ApplicationConfig._shared_state.clear()

    def test_descriptor_value_is_shared(self):
        a = ApplicationConfig()
        b = ApplicationConfig()
        a.debug = True
        self.assertTrue(b.debug)

    def test_cannot_delete_shared_attribute(self):
        config = ApplicationConfig()
        with self.assertRaises(AttributeError):
            del config.debug

    def test_descriptor_returns_itself_on_class_access(self):
        descriptor = ApplicationConfig.debug
        self.assertIsInstance(descriptor, ThreadSafeSharedAttribute)

    def test_concurrent_writes_do_not_crash(self):
        config = ApplicationConfig()

        def worker(index: int):
            for _ in range(1000):
                config.pool_size = index

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertIn(config.pool_size, range(10))

    def test_multiple_instances_see_same_descriptor_value(self):
        a = ApplicationConfig()
        b = ApplicationConfig()
        c = ApplicationConfig()
        a.db_url = "postgresql://localhost:5432/app"
        self.assertEqual(b.db_url, "postgresql://localhost:5432/app")
        self.assertEqual(c.db_url, "postgresql://localhost:5432/app")


if __name__ == "__main__":
    unittest.main()
