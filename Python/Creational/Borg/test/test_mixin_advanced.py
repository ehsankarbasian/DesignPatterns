from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from borg_mixin_advanced import SharedStateMixin


class Logger(SharedStateMixin):
    pass

class Config(SharedStateMixin):
    pass


class Service:
    def __init__(self):
        self.initialized = True


class AdvancedLogger(SharedStateMixin, Service):
    pass


class BorgMixinAdvancedTestCase(TestCase):

    def test_instances_share_state(self):
        a = Logger()
        b = Logger()
        a.value = 10
        self.assertEqual(b.value, 10)

    def test_subclasses_have_separate_state(self):
        logger = Logger()
        config = Config()
        logger.level = "INFO"
        self.assertFalse(hasattr(config, "level"))
    
    def test_subclasses_have_separate_states_shared(self):
        logger_1 = Logger()
        logger_2 = Logger()
        config_1 = Config()
        config_2 = Config()
        
        logger_1.level = "INFO"
        config_2.debug = True
        
        self.assertTrue(hasattr(logger_1, "level"))
        self.assertTrue(hasattr(logger_2, "level"))
        self.assertEqual(logger_1.level, "INFO")
        self.assertEqual(logger_2.level, "INFO")
        self.assertFalse(hasattr(config_1, "level"))
        self.assertFalse(hasattr(config_2, "level"))
        
        self.assertTrue(hasattr(config_1, "debug"))
        self.assertTrue(hasattr(config_2, "debug"))
        self.assertTrue(config_1.debug)
        self.assertTrue(config_2.debug)
        self.assertFalse(hasattr(logger_1, "debug"))
        self.assertFalse(hasattr(logger_2, "debug"))
        
        self.assertEqual(logger_1.__dict__, logger_2.__dict__)
        self.assertEqual(config_1.__dict__, config_2.__dict__)
        self.assertNotEqual(logger_1.__dict__, config_2.__dict__)
        self.assertNotEqual(id(logger_1.__dict__), id(config_2.__dict__))
        self.assertNotEqual(logger_1.__dict__, config_1.__dict__)
        self.assertNotEqual(id(logger_1.__dict__), id(config_1.__dict__))
        self.assertNotEqual(logger_2.__dict__, config_2.__dict__)
        self.assertNotEqual(id(logger_2.__dict__), id(config_2.__dict__))
        self.assertNotEqual(logger_2.__dict__, config_1.__dict__)
        self.assertNotEqual(id(logger_2.__dict__), id(config_1.__dict__))
        

    def test_state_is_same_dict(self):
        a = Logger()
        b = Logger()
        self.assertIs(a.__dict__, b.__dict__)

    def test_multiple_inheritance_super_init(self):
        obj = AdvancedLogger()
        self.assertTrue(obj.initialized)

    def test_state_persists_between_instances(self):
        a = Logger()
        a.count = 5
        b = Logger()
        self.assertEqual(b.count, 5)


if __name__ == "__main__":
    unittest.main()
