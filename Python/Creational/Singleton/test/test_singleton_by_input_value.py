from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from singleton_by_input_value import Logger


class SingletonByInputValueTestCase(TestCase):
    
    def setUp(self):
        self.logger_1 = Logger(log_file='file_1')
        self.logger_2 = Logger(log_file='file_2')
        return super().setUp()
    
    def test_differs_by_value(self):
        self.assertNotEqual(self.logger_1, self.logger_2)
    
    def test_singleton_by_value(self):
        another_logger_1 = Logger(log_file='file_1')
        self.assertEqual(self.logger_1, another_logger_1)
        self.assertEqual(id(self.logger_1), id(another_logger_1))


if __name__=='__main__':
    unittest.main()
