from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

import threading
from threadsafe_examples.mixin import ThreadSafeBorgMixin, AppConfig


class ThreadSafeBorgMixinTestCase(TestCase):

    def setUp(self):
        ThreadSafeBorgMixin._shared_state.clear()

    def test_instances_are_different_objects(self):
        a = AppConfig("A")
        b = AppConfig("B")
        self.assertIsNot(a, b)

    def test_state_is_shared_between_instances(self):
        a = AppConfig("A")
        b = AppConfig("B")
        a.set_shared("mode", "production")
        self.assertEqual(b.get_shared("mode"), "production")

    def test_thread_safety_under_concurrency(self):
        config = AppConfig("main")

        def worker(i: int):
            for _ in range(1000):
                config.set_shared("counter", i)

        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(10)
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        result = config.get_shared("counter")
        self.assertIn(result, range(10))


if __name__ == "__main__":
    unittest.main()
