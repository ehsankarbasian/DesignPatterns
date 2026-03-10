from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from borg_descriptor import Borg


class TestBorgSharedAttribute(TestCase):

    def setUp(self):
        # reset shared state before each test
        Borg._shared_state.clear()
        Borg.counter.value = 0

    def test_shared_counter_between_instances(self):
        a = Borg()
        b = Borg()
        a.counter = 10
        self.assertEqual(b.counter, 10)
    
    def test_state_value_is_available_via_class(self):
        a = Borg()
        a.counter = 10
        self.assertEqual(Borg.counter.value, 10)

    def test_validation_rejects_negative(self):
        a = Borg()
        with self.assertRaises(ValueError):
            a.counter = -1

    def test_delete_not_allowed(self):
        a = Borg()
        with self.assertRaises(AttributeError):
            del a.counter


if __name__=='__main__':
    unittest.main()
