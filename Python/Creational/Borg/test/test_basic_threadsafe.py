from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

import threading
from threadsafe_examples.basic import ThreadSafeBorg


class TestThreadSafeBorg(TestCase):

    def test_borg_shared_state(self):
        a = ThreadSafeBorg()
        b = ThreadSafeBorg()
        a.set("mode", "prod")
        self.assertEqual(b.get("mode"), "prod")

    def test_borg_thread_safety(self):
        borg = ThreadSafeBorg()

        def worker(idx: int):
            for _ in range(1000):
                borg.set("counter", idx)

        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(10)
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertIn(borg.get("counter"), range(10))


if __name__ == "__main__":
    unittest.main()
