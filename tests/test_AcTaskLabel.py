import json
import time
from unittest import TestCase

from AcTaskLabel import AcTaskLabel


class TestAcTaskLabel(TestCase):

    @staticmethod
    def _generate_test_task_label(label_id: int) -> AcTaskLabel:
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
        self.assertEqual(label_id, label.id)

    def test_to_dict(self):
        label_id = 746
        label = self._generate_test_task_label(label_id)
        label_dict = label.to_dict()
        self.assertEqual(label_id, label_dict["id"])
        self.assertEqual("TaskLabel", label_dict["class"])

    def test_to_json(self):
        label_id = 747
        label = self._generate_test_task_label(label_id)
        label_json = label.to_json()
        self.assertEqual(label_id, json.loads(label_json)["id"])
        self.assertEqual("TaskLabel", json.loads(label_json)["class"])
