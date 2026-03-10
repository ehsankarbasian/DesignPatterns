import unittest

from test_singleton_threadsafe import SingletonPatternThreadSafeTestCase
from test_abstract_singleton import SingletonABCPatternTestCase

from singleton_thread_safe import SingletonABCPatternThreadSafe


class ThreadSafeTestCase(SingletonPatternThreadSafeTestCase):
    _SETUP_META_SINGLETON = SingletonABCPatternThreadSafe
    
    def setUp(self):
        return super().setUp()


class AbstractTestCase(SingletonABCPatternTestCase):
    _SETUP_META_SINGLETON = SingletonABCPatternThreadSafe
    
    def setUp(self):
        return super().setUp()


if __name__=='__main__':
    unittest.main()
