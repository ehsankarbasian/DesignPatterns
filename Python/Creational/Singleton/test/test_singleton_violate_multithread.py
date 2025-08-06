from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from threading import Thread
from time import sleep
from singleton_thread_safe import SingletonPatternThreadSafe


class SingletonPatternTestCase(TestCase):
    
    def setUp(self):
        class BlahBlah(metaclass=SingletonPatternThreadSafe):
            pass
        class BlahBlahChild(BlahBlah):
            pass
        
        self.blah_1 = BlahBlah()
        self.blah_2 = BlahBlah()
        self.blah_child_1 = BlahBlahChild()
        self.blah_child_2 = BlahBlahChild()
        
        class Foo(metaclass=SingletonPatternThreadSafe):
            def __init__(self, value):
                self.value = value
        
        # self.foo = Foo(value=None)
        self.Foo = Foo
    
    def tearDown(self):
        pass
    
    # def test_singleton_without_thread(self):
    #     self.assertEqual(self.blah_1, self.blah_2)
    
    # def test_singleton_for_childs_without_thread(self):
    #     self.assertEqual(self.blah_child_1, self.blah_child_2)
    
    # def test_not_equal_different_classes_without_thread(self):
    #     self.assertNotEqual(self.blah_1, self.foo)
    
    # def test_not_equal_parent_and_child_without_thread(self):
    #     self.assertNotEqual(self.blah_1, self.blah_child_1)
    
    def _test_singleton(self, value):
        if value == 1:
            print(f'thread 1 waith 1 seconds before call class')
            sleep(1)
        foo = self.Foo(value=value)
        self.__setattr__(f'foo_id_{value}', id(foo))
    
    def test_singleton_with_thread(self):
        process1 = Thread(target=self._test_singleton, args=(1,))
        process2 = Thread(target=self._test_singleton, args=(2,))
        process1.start()
        process2.start()
        sleep(4)
        foo_id_1 = int(self.foo_id_1)
        foo_id_2 = int(self.foo_id_2)
        self.assertEqual(foo_id_1, foo_id_2)


if __name__=='__main__':
    unittest.main()
