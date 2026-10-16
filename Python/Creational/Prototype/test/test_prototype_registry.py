from unittest import TestCase
import unittest

import pathlib
import sys

path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from prototype_registry import (
    ChartWidget,
    TableWidget,
    UnknownPrototypeError,
    WidgetRegistry,
)


class PrototypeRegistryTestCase(TestCase):

    def setUp(self):
        self.registry = WidgetRegistry()

        self.chart = ChartWidget(
            title="Revenue",
            chart_type="bar",
            refresh_interval=30,
            filters=["region", "department"],
        )
        self.table = TableWidget(
            title="Audit Log",
            refresh_interval=60,
            columns=["timestamp", "actor", "action"],
            settings={"page_size": "20", "compact": "true"},
        )

        self.registry.register("revenue-chart", self.chart)
        self.registry.register("audit-table", self.table)

        super().setUp()

    def tearDown(self):
        del self.registry
        del self.chart
        del self.table
        super().tearDown()

    def test_registry_can_store_multiple_prototypes(self):
        self.assertTrue("revenue-chart" in self.registry._prototypes)
        self.assertTrue("audit-table" in self.registry._prototypes)

    def test_contains_reports_registration_presence(self):
        self.assertTrue(self.registry.contains("revenue-chart"))
        self.assertFalse(self.registry.contains("unknown-widget"))

    def test_clone_creates_new_instance(self):
        cloned_chart = self.registry.clone("revenue-chart")

        self.assertNotEqual(id(cloned_chart), id(self.chart))

    def test_clone_preserves_values(self):
        cloned_chart = self.registry.clone("revenue-chart")

        self.assertEqual(cloned_chart.title, self.chart.title)
        self.assertEqual(cloned_chart.chart_type, self.chart.chart_type)
        self.assertEqual(cloned_chart.refresh_interval, self.chart.refresh_interval)
        self.assertEqual(cloned_chart.filters, self.chart.filters)

    def test_multiple_clones_are_independent(self):
        clone1 = self.registry.clone("revenue-chart")
        clone2 = self.registry.clone("revenue-chart")

        self.assertNotEqual(id(clone1), id(clone2))
        self.assertNotEqual(id(clone1.filters), id(clone2.filters))

    def test_modifying_clone_does_not_affect_prototype(self):
        clone = self.registry.clone("revenue-chart")

        clone.title = "Updated Revenue"
        clone.filters.append("new-dimension")

        self.assertNotEqual(clone.title, self.chart.title)
        self.assertNotIn("new-dimension", self.chart.filters)

    def test_unregister_removes_prototype(self):
        self.registry.unregister("revenue-chart")

        self.assertFalse(self.registry.contains("revenue-chart"))
        with self.assertRaises(UnknownPrototypeError):
            self.registry.clone("revenue-chart")


if __name__ == "__main__":
    unittest.main()
