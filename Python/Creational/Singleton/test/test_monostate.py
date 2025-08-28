from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from monostate import Book


class SingletonByInputValueTestCase(TestCase):
    
    def setUp(self):
        self.book_1 = Book()
        self.book_2 = Book()
        self.book_3 = Book()
        self.book_1.x = "200"
        self.book_1.y = "rangi"
        self.book_2.x = "300"
        self.book_3.z = "20"
        return super().setUp()
    
    def test_different_instances(self):
        self.assertNotEqual(self.book_1, self.book_2)
        self.assertNotEqual(self.book_2, self.book_3)
    
    def test_same_state(self):
        self.assertEqual(self.book_1.__dict__, self.book_2.__dict__)
        self.assertEqual(self.book_2.__dict__, self.book_3.__dict__)
    
    def test_same_attriburtes(self):
        self.assertEqual(self.book_1.x, self.book_2.x)
        self.assertEqual(self.book_1.y, self.book_2.y)
        self.assertEqual(self.book_1.z, self.book_2.z)
        self.assertEqual(self.book_2.x, self.book_3.x)
        self.assertEqual(self.book_2.y, self.book_3.y)
        self.assertEqual(self.book_2.z, self.book_3.z)
    
    def test_attributes_are_shared(self):
        self.book_3.x = 5
        self.assertEqual(self.book_1.x, 5)
        self.book_2.x = 10
        self.assertEqual(self.book_1.x, 10)


if __name__=='__main__':
    unittest.main()
