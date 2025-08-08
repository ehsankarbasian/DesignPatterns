from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

import copy


class _InnerAttr:
            pass
        
class _Attr:
    def __init__(self, inner_attr):
        self.inner_attr = inner_attr

class _Obj:
    def __init__(self, attr):
        self.attr = attr


class SingletonPatternTestCase(TestCase):
    
    def setUp(self):
        self.inner_attr = _InnerAttr()
        self.attr = _Attr(inner_attr = self.inner_attr)
        self.obj = _Obj(attr=self.attr)
    
    def tearDown(self):
        del self.obj
        del self.attr
        del self.inner_attr
    
    def test_instance_changes_with_shallowcopy(self):
        old_obj_id = id(self.obj)
        obj_copy = copy.copy(self.obj)
        new_obj_id = id(obj_copy)
        self.assertNotEqual(old_obj_id, new_obj_id)
    
    def test_instance_attr_not_changes_with_shallowcopy(self):
        old_attr_id = id(self.obj.attr)
        obj_copy = copy.copy(self.obj)
        new_attr_id = id(obj_copy.attr)
        self.assertEqual(old_attr_id, new_attr_id)
    
    def test_instance_inner_attr_not_changes_with_shallowcopy(self):
        old_inner_attr_id = id(self.obj.attr.inner_attr)
        obj_copy = copy.copy(self.obj)
        new_inner_attr_id = id(obj_copy.attr.inner_attr)
        self.assertEqual(old_inner_attr_id, new_inner_attr_id)
    
    def test_instance_changes_with_deepcopy(self):
        old_obj_id = id(self.obj)
        obj_copy = copy.deepcopy(self.obj)
        new_obj_id = id(obj_copy)
        self.assertNotEqual(old_obj_id, new_obj_id)
    
    def test_instance_attr_changes_with_deepcopy(self):
        old_attr_id = id(self.obj.attr)
        obj_copy = copy.deepcopy(self.obj)
        new_attr_id = id(obj_copy.attr)
        self.assertNotEqual(old_attr_id, new_attr_id)
    
    def test_instance_inner_attr_changes_with_deepcopy(self):
        old_inner_attr_id = id(self.obj.attr.inner_attr)
        obj_copy = copy.deepcopy(self.obj)
        new_inner_attr_id = id(obj_copy.attr.inner_attr)
        self.assertNotEqual(old_inner_attr_id, new_inner_attr_id)
    
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

