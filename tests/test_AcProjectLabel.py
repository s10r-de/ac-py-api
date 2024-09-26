import json
import time
from unittest import TestCase

from AcProjectLabel import AcProjectLabel


class TestAcProjectLabel(TestCase):

    def _generate_test_project_label(self, label_id: int) -> AcProjectLabel:
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
            project_id=56
        )

    def test_constructor(self):
        label_id = 735
        label = self._generate_test_project_label(label_id)
        self.assertEqual(label.id, label_id)

    def test_to_dict(self):
        label_id = 736
        label = self._generate_test_project_label(label_id)
        label_dict = label.to_dict()
        self.assertEqual(label_dict["id"], label_id)
        self.assertEqual(label_dict["class"], "ProjectLabel")

    def test_to_json(self):
        label_id = 737
        label = self._generate_test_project_label(label_id)
        label_json = label.to_json()
        self.assertEqual(json.loads(label_json)["id"], label_id)
        self.assertEqual(json.loads(label_json)["class"], "ProjectLabel")
