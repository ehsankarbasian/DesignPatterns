from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from borg_mixin import Logger, Config


class TestSharedStateMixin(TestCase):

    def setUp(self):
        Logger._shared_state.clear()

    def test_state_shared_between_classes(self):
        logger = Logger()
        config = Config()
        logger.shared_value = 42
        self.assertEqual(config.shared_value, 42)

    def test_state_shared_between_instances(self):
        a = Logger()
        b = Logger()
        a.test = "value"
        self.assertEqual(b.test, "value")
        
    def test_classes_share_same_dict(self):
        logger = Logger()
        config = Config()
        self.assertEqual(id(logger.__dict__), id(config.__dict__))
        
    def test_instances_share_same_dict(self):
        a = Logger()
        b = Logger()
        self.assertEqual(id(a.__dict__), id(b.__dict__))


if __name__ == "__main__":
    unittest.main()
