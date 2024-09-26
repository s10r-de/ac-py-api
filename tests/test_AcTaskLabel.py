import json
import time
from unittest import TestCase

from AcTaskLabel import AcTaskLabel


class TestAcTaskLabel(TestCase):

    def _generate_test_task_label(self, label_id: int) -> AcTaskLabel:
        return AcTaskLabel(
            id=label_id,
            class_="TaskLabel",
            url_path="/task/label/%d" % label_id,
            name="Test Task Label",
            updated_on=int(time.time()),
            color="#ff00ff",
            lighter_text_color="#ffa0ff",
            darker_text_color="#a0a0a0",
            is_default=True,
            is_global=True,
            position=3,
            project_id=34
        )

    def test_constructor(self):
        label_id = 745
        label = self._generate_test_task_label(label_id)
        self.assertEqual(label.id, label_id)

    def test_to_dict(self):
        label_id = 746
        label = self._generate_test_task_label(label_id)
        label_dict = label.to_dict()
        self.assertEqual(label_dict["id"], label_id)
        self.assertEqual(label_dict["class"], "TaskLabel")

    def test_to_json(self):
        label_id = 747
        label = self._generate_test_task_label(label_id)
        label_json = label.to_json()
        self.assertEqual(json.loads(label_json)["id"], label_id)
        self.assertEqual(json.loads(label_json)["class"], "TaskLabel")
