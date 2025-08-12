from inspect import isabstract
from abc import abstractmethod
from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from singleton import SingletonABCPattern


class SingletonABCPatternTestCase(TestCase):
    
    def setUp(self):
        class AbstractSingletonBlahBlah(metaclass=SingletonABCPattern):
            @property
            @abstractmethod
            def p(self):
                pass
        class BlahBlah(AbstractSingletonBlahBlah):
            p = 'blah'
        class Foo(AbstractSingletonBlahBlah):
            p = 'foo'
        
        self.AbstractSingleton = AbstractSingletonBlahBlah
        self.BlahBlah = BlahBlah
        self.blah_1 = BlahBlah()
        self.blah_2 = BlahBlah()
        self.foo_1 = Foo()
        self.foo_2 = Foo()
        
        class BlahBlahChild(BlahBlah):
            pass
        self.blah_child_1 = BlahBlahChild()
        self.blah_child_2 = BlahBlahChild()
        super().setUp()
    
    def tearDown(self):
        super().tearDown()
    
    def test_is_abstract(self):
        self.assertTrue(isabstract(self.AbstractSingleton))
    
    def test_implementor_is_not_abstract(self):
        self.assertFalse(isabstract(self.BlahBlah))
    
    def test_singleton(self):
        self.assertEqual(self.blah_1, self.blah_2)
        self.assertEqual(self.foo_1, self.foo_2)
    
    def test_singleton_for_childs(self):
        self.assertEqual(self.blah_child_1, self.blah_child_2)
    
    def test_not_equal_different_implementors(self):
        self.assertNotEqual(self.blah_1, self.foo_1)
    
    def test_not_equal_parent_and_child(self):
        self.assertNotEqual(self.blah_1, self.blah_child_1)


if __name__=='__main__':
    unittest.main()
