from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from threading import Thread
from time import sleep
from singleton_violating_multithread import SingletonPatternThreadSafeToViolate


class SingletonPatternNotThreadSafeTestCase(TestCase):
    
    def setUp(self):
        class Foo(metaclass=SingletonPatternThreadSafeToViolate):
            def __init__(self, value):
                self.value = value
        
        self.Foo = Foo
        super().setUp()
    
    def tearDown(self):
        super().tearDown()
    
    def _test_singleton(self, value):
        if value == 1:
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
        self.assertNotEqual(foo_id_1, foo_id_2)


if __name__=='__main__':
    unittest.main()
