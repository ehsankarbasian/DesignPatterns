from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

import copy


class SingletonPatternTestCase(TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_pointer_not_changes_with_assignment(self):
        final_list = []
        temp_list = [1, 2, 3]
        final_list.append(temp_list)
        temp_list.append(4)
        self.assertEqual(final_list[0], temp_list)
        self.assertEqual(id(final_list[0]), id(temp_list))
    
    def test_general_pointer_changes_with_shallowcopy(self):
        my_list = [1, 2, 3]
        new_list = my_list.copy()
        my_list[-1] = 9
        self.assertNotEqual(my_list[-1], new_list[-1])
        self.assertNotEqual(id(my_list[-1]), id(new_list[-1]))
    
    def test_inner_pointer_not_changes_with_shallowcopy(self):
        my_list = [[1, 2, 3], [4, 5, 6], 7, 8]
        new_list = my_list.copy()
        my_list[-1] = 9
        my_list[1][1] = 2
        self.assertEqual(new_list[1][1], my_list[1][1])
        self.assertEqual(id(new_list[1][1]), id(my_list[1][1]))
    
    def test_inner_pointer_changes_with_deepcopy(self):
        my_list = [[1, 3], [4, 5, 6], 7, 8]
        new_list = copy.deepcopy(my_list)
        my_list[-1] = 9
        my_list[1][1] = 2
        self.assertEqual(new_list[-1], 8)
        self.assertEqual(my_list[-1], 9)
        self.assertEqual(new_list[1][1], 5)
        self.assertEqual(my_list[1][1], 2)
        self.assertNotEqual(new_list[-1], my_list[-1])
        self.assertNotEqual(new_list[1][1], my_list[1][1])
    
    def test_list_comprehansion(self):
        final_list = []
        temp_list = [1, 2, 3]
        final_list = [i for i in temp_list]
        temp_list.append(4)
        self.assertEqual(final_list[-1], 3)
        self.assertEqual(temp_list[-1], 4)


if __name__=='__main__':
    unittest.main()

