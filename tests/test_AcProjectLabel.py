import json
import time
from unittest import TestCase

from active_collab_api.AcProjectLabel import AcProjectLabel
from active_collab_api import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


class TestAcProjectLabel(TestCase):
    @staticmethod
    def _generate_test_project_label(label_id: int) -> AcProjectLabel:
        return AcProjectLabel(
            id=label_id,
            class_="ProjectLabel",
            url_path="/projects/label/%d" % label_id,
            name="Test Project Label",
            updated_on=int(time.time()),
            color="#ff00ff",
            lighter_text_color="#ffa0ff",
            darker_text_color="#a0a0a0",
            is_default=True,
            position=1,
            project_id=56,
        )

    def test_constructor(self):
        label_id = 735
        label = self._generate_test_project_label(label_id)
        self.assertEqual(label_id, label.id)

    def test_to_dict(self):
        label_id = 736
        label = self._generate_test_project_label(label_id)
        label_dict = label.to_dict()
        self.assertEqual(label_id, label_dict["id"])
        self.assertEqual(
            "ProjectLabel",
            label_dict["class"],
        )
        self.assertIn(AC_PROPERTY_CLASS, label_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, label_dict.keys())

    def test_to_json(self):
        label_id = 737
        label = self._generate_test_project_label(label_id)
        label_json = label.to_json()
        self.assertEqual(label_id, json.loads(label_json)["id"])
        self.assertEqual(
            "ProjectLabel",
            json.loads(label_json)["class"],
        )
        self.assertIn(AC_PROPERTY_CLASS, json.loads(label_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(label_json).keys())
