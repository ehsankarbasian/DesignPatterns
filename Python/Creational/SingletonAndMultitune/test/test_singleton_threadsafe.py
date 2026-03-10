from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from threading import Thread
from singleton_thread_safe import SingletonPatternThreadSafe


class SingletonPatternThreadSafeTestCase(TestCase):
    _FIRST_FOO_VALUE = "FOO"
    _SETUP_META_SINGLETON = SingletonPatternThreadSafe
    
    def setUp(self):
        class BlahBlah(metaclass=self._SETUP_META_SINGLETON):
            pass
        class BlahBlahChild(BlahBlah):
            pass
        
        self.blah_1 = BlahBlah()
        self.blah_2 = BlahBlah()
        self.blah_child_1 = BlahBlahChild()
        self.blah_child_2 = BlahBlahChild()
        
        class Foo(metaclass=self._SETUP_META_SINGLETON):
            def __init__(self, value):
                self.value = value
        
        self.Foo = Foo
        super().setUp()
    
    def tearDown(self):
        super().tearDown()
    
    def _test_singleton(self, value, results):
        foo = self.Foo(value=value)
        results.append(id(foo))
    
    def test_singleton_with_thread(self):
        instance_ids = []

        thread_1 = Thread(target=self._test_singleton, args=(self._FIRST_FOO_VALUE, instance_ids))
        thread_2 = Thread(target=self._test_singleton, args=("BAR", instance_ids))

        thread_1.start()
        thread_2.start()
        thread_1.join()
        thread_2.join()

        self.assertEqual(
            len(set(instance_ids)),
            1,
            "Singleton is not thread-safe: multiple instances created"
        )
    
    def test_singleton_without_thread(self):
        self.assertEqual(self.blah_1, self.blah_2)
    
    def test_singleton_for_childs_without_thread(self):
        self.assertEqual(self.blah_child_1, self.blah_child_2)
    
    def test_not_equal_different_classes_without_thread(self):
        self.assertNotEqual(self.blah_1, self.Foo(value='BLAH'))
    
    def test_not_equal_parent_and_child_without_thread(self):
        self.assertNotEqual(self.blah_1, self.blah_child_1)


if __name__=='__main__':
    unittest.main()
