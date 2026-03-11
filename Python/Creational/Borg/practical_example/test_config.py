from unittest import TestCase
import unittest

import threading

from config import Config
from descriptors import SharedField


class ConfigSharedStateTestCase(TestCase):

    def setUp(self):
        # Reset shared state before each test to avoid cross‑test pollution.
        Config.db_url._value = Config.db_url.default
        Config.debug._value = Config.debug.default
        Config.api_key._value = Config.api_key.default
        Config.timeout._value = Config.timeout.default
        Config.max_retries._value = Config.max_retries.default


    def test_shared_state_between_instances(self):
        # Changes in one instance must be visible in another.
        c1 = Config()
        c2 = Config()
        c1.debug = True
        self.assertTrue(c2.debug)


    def test_attribute_set_and_get(self):
        # Setting a value should update the shared descriptor state.
        c = Config()
        c.timeout = 99
        self.assertEqual(c.timeout, 99)


    def test_delete_resets_to_default(self):
        c = Config()
        c.timeout = 100
        del c.timeout
        self.assertEqual(c.timeout, 30)


    def test_descriptor_access_from_class(self):
        # Accessing the attribute via the class should return the descriptor.
        descriptor = Config.db_url
        self.assertIsInstance(descriptor, SharedField)


    def test_shared_mutation_across_instances(self):
        c1 = Config()
        c2 = Config()
        c1.db_url = "postgresql://prod-db"
        self.assertEqual(c2.db_url, "postgresql://prod-db")


    def test_basic_thread_access(self):
        """
        Multiple threads writing values should not crash
        and final value should be one of the written values.
        """

        config = Config()

        def worker(value):
            for _ in range(1000):
                config.timeout = value

        threads = [
            threading.Thread(target=worker, args=(10,)),
            threading.Thread(target=worker, args=(20,))
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertIn(config.timeout, [10, 20])


if __name__ == "__main__":
    unittest.main()
