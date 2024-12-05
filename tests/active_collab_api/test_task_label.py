import json
import time
from unittest import TestCase

from active_collab_api import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_
from active_collab_api.ac_task_label import (
    AcTaskLabel,
    task_label_from_json,
    task_label_from_task_json,
)


class TestAcTaskLabel(TestCase):
    @staticmethod
    def _generate_test_task_label(label_id: int) -> AcTaskLabel:
        return AcTaskLabel(
            id=label_id,
            class_="TaskLabel",
            url_path=f"/task/label/{label_id}",
            name="Test Task Label",
            updated_on=int(time.time()),
            color="#ff00ff",
            lighter_text_color="#ffa0ff",
            darker_text_color="#a0a0a0",
            is_default=True,
            is_global=True,
            position=3,
            project_id=34,
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
        self.assertIn(AC_PROPERTY_CLASS, label_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, label_dict.keys())

    def test_to_json(self):
        label_id = 747
        label = self._generate_test_task_label(label_id)
        label_json = label.to_json()
        self.assertEqual(label_id, json.loads(label_json)["id"])
        self.assertEqual("TaskLabel", json.loads(label_json)["class"])
        self.assertIn(AC_PROPERTY_CLASS, json.loads(label_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(label_json).keys())

    def test_from_json(self):
        label_id = 763
        task_json = {
            "id": label_id,
            "class": "TaskLabel",
            "url_path": f"/task/label/{label_id}",
            "name": "Test Task Label",
            "updated_on": int(time.time()),
            "color": "#ff00ff",
            "lighter_text_color": "#ffa0ff",
            "darker_text_color": "#a0a0a0",
            "is_default": True,
            "is_global": True,
            "position": 3,
            "project_id": 34,
        }
        task_label = task_label_from_json(task_json)
        self.assertEqual(label_id, task_label.id)
        self.assertEqual("TaskLabel", task_label.class_)

    def test_from_task_json(self):
        label_id = 769
        task_json = {
            "class": "TaskLabel",
            "color": "#C3E799",
            "darker_text_color": "#718658",
            "id": label_id,
            "is_default": False,
            "is_global": True,
            "lighter_text_color": "#80C333",
            "name": "WONT FIX",
            "position": "5",
            "project_id": None,
            "updated_on": None,
            "url_path": "/labels/61",
        }

        task_label = task_label_from_task_json(task_json)
        self.assertEqual(label_id, task_label.id)
        self.assertEqual("TaskLabel", task_label.class_)

    def test_from_task_json_without_class_property(self):
        data = {
            "id": 33,
            "name": "NEW",
            "color": "#C3E799",
            "lighter_text_color": "#80C333",
            "darker_text_color": "#718658",
        }
        task_label = task_label_from_task_json(data)
        self.assertEqual(33, task_label.id)
        self.assertEqual("TaskLabel", task_label.class_)
