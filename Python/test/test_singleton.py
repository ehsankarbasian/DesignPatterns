from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from singleton import SingletonPattern


class SingletonPatternTestCase(TestCase):
    
    def setUp(self):
        class Foo(metaclass=SingletonPattern):
            pass
        class BlahBlah(metaclass=SingletonPattern):
            pass
        class BlahBlahChild(BlahBlah):
            pass
        
        self.foo = Foo()
        self.blah_1 = BlahBlah()
        self.blah_2 = BlahBlah()
        
        self.blah_child_1 = BlahBlahChild()
        self.blah_child_2 = BlahBlahChild()
    
    def tearDown(self):
        pass
    
    def test_singleton(self):
        self.assertEqual(self.blah_1, self.blah_2)
    
    def test_singleton_for_childs(self):
        self.assertEqual(self.blah_child_1, self.blah_child_2)
    
    def test_not_equal_different_classes(self):
        self.assertNotEqual(self.blah_1, self.foo)
    
    def test_not_equal_parent_and_child(self):
        self.assertNotEqual(self.blah_1, self.blah_child_1)


if __name__=='__main__':
    unittest.main()
