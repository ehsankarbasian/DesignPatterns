from unittest import TestCase
import unittest

import copy

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from advanced_example import SelfReferencingEntity, SomeComponent


class ShallowCopyTestCase(TestCase):
    
    def setUp(self):
        list_of_objects = [1, {1, 2, 3}, [1, 2, 3]]
        circular_ref = SelfReferencingEntity()
        self.component = SomeComponent(23, list_of_objects, circular_ref)
        circular_ref.set_parent(self.component)
        self.shallow_copied_component = copy.copy(self.component)
        super().setUp()
    
    def tearDown(self):
        super().tearDown()
    
    def test_component_attr_changes(self):
        self.shallow_copied_component.some_list_of_objects.append("another object")
        self.assertEqual(self.component.some_list_of_objects[-1], "another object")
    
    def test_shallow_copied_component_attr_changes(self):
        self.component.some_list_of_objects[1].add(4)
        self.assertTrue(4 in self.shallow_copied_component.some_list_of_objects[1])


class DeepCopyTestCase(TestCase):
    
    def setUp(self):
        list_of_objects = [1, {1, 2, 3}, [1, 2, 3]]
        circular_ref = SelfReferencingEntity()
        self.component = SomeComponent(23, list_of_objects, circular_ref)
        circular_ref.set_parent(self.component)
        self.deep_copied_component = copy.deepcopy(self.component)
        super().setUp()
    
    def tearDown(self):
        super().tearDown()
    
    def test_component_attr_not_changes(self):
        self.deep_copied_component.some_list_of_objects.append("one more object")
        self.assertNotEqual(self.component.some_list_of_objects[-1], "one more object")
    
    def test_deep_copied_component_attr_not_changes(self):
        self.component.some_list_of_objects[1].add(10)
        self.assertTrue(10 not in self.deep_copied_component.some_list_of_objects[1])
    
    def test_circular_ref_not_cloned_repeatedly(self):
        id_1 = id(self.deep_copied_component.some_circular_ref.parent)
        id_2 = id(self.deep_copied_component.some_circular_ref.parent.some_circular_ref.parent)
        self.assertEqual(id_1, id_2)


if __name__ == "__main__":
    unittest.main()
