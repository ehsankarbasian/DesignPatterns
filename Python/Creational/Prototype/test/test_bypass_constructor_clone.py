import copy
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from bypass_constructor_clone import ReportTemplate


class ReportTemplateCloneTest(unittest.TestCase):

    def setUp(self):
        super().setUp()
        ReportTemplate.constructor_call_count = 0
        self.source = ReportTemplate("Annual Audit", ["Summary", "Details"])

    def tearDown(self):
        del self.source
        ReportTemplate.constructor_call_count = 0
        super().tearDown()

    def test_constructor_increments_counter(self):
        self.assertEqual(ReportTemplate.constructor_call_count, 1)

    def test_clone_bypasses_constructor(self):
        clone = self.source.clone()
        self.assertEqual(ReportTemplate.constructor_call_count, 1)
        self.assertIsNot(clone, self.source)

    def test_clone_resets_instance_specific_state(self):
        self.source.render()
        self.assertEqual(self.source.render_count, 1)

        clone = self.source.clone()
        self.assertEqual(clone.instance_label, "clone")
        self.assertEqual(clone.render_count, 0)

    def test_raw_deepcopy_retains_source_instance_state(self):
        self.source.render()
        raw_copy = copy.deepcopy(self.source)

        self.assertEqual(ReportTemplate.constructor_call_count, 1)
        self.assertEqual(raw_copy.instance_label, "source")
        self.assertEqual(raw_copy.render_count, 1)

    def test_clone_preserves_template_data(self):
        clone = self.source.clone()
        self.assertEqual(clone.title, self.source.title)
        self.assertEqual(clone.sections, self.source.sections)
        self.assertEqual(clone.layout, self.source.layout)

    def test_modifying_clone_does_not_affect_source(self):
        clone = self.source.clone()
        clone.render()

        self.assertEqual(clone.render_count, 1)
        self.assertEqual(self.source.render_count, 0)

    def test_render_output_format(self):
        rendered = self.source.render()
        self.assertIn("Report 'Annual Audit' [source]", rendered)
        self.assertIn("renders=1", rendered)

    def test_describe_contains_all_state_fields(self):
        desc = self.source.describe()
        self.assertIn("Annual Audit", desc)
        self.assertIn("source", desc)
        self.assertIn("render_count=0", desc)


if __name__ == "__main__":
    unittest.main()
