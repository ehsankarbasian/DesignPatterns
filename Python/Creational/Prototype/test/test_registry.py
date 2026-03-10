from unittest import TestCase
import unittest

import pathlib
import sys

path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from prototype_with_registry import ShapeRegistry, Rectangle, Circle


class PrototypeRegistryTestCase(TestCase):

    def setUp(self):
        self.registry = ShapeRegistry()

        self.rectangle = Rectangle(10, 20)
        self.circle = Circle(5)

        self.registry.register("rectangle", self.rectangle)
        self.registry.register("circle", self.circle)

        super().setUp()

    def tearDown(self):
        del self.registry
        del self.rectangle
        del self.circle
        super().tearDown()

    def test_registry_can_store_multiple_prototypes(self):
        self.assertTrue("rectangle" in self.registry._prototypes)
        self.assertTrue("circle" in self.registry._prototypes)

    def test_clone_creates_new_instance(self):
        cloned_rectangle = self.registry.clone("rectangle")

        self.assertNotEqual(id(cloned_rectangle), id(self.rectangle))

    def test_clone_preserves_values(self):
        cloned_rectangle = self.registry.clone("rectangle")

        self.assertEqual(cloned_rectangle.width, self.rectangle.width)
        self.assertEqual(cloned_rectangle.height, self.rectangle.height)

    def test_multiple_clones_are_independent(self):
        clone1 = self.registry.clone("circle")
        clone2 = self.registry.clone("circle")

        self.assertNotEqual(id(clone1), id(clone2))

    def test_modifying_clone_does_not_affect_prototype(self):
        clone = self.registry.clone("rectangle")

        clone.width = 999

        self.assertNotEqual(clone.width, self.rectangle.width)

    def test_unregister_removes_prototype(self):
        self.registry.unregister("circle")

        with self.assertRaises(KeyError):
            self.registry.clone("circle")


if __name__ == "__main__":
    unittest.main()
