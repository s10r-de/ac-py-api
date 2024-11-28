import json
from unittest import TestCase

from ActiveCollabAPI.AcTaskList import task_list_from_json, AcTaskList
from ActiveCollabAPI import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


class TestAcTaskList(TestCase):
    @staticmethod
    def _generate_test_task_list(task_list_id: int) -> AcTaskList:
        with open("example-data/example-task-list-37314.json", "r") as fh:
            task_list = task_list_from_json(json.load(fh))
        task_list.id = task_list_id
        return task_list

    def test_actasklist_constructor(self):
        task_list_id = 37614
        task_list = self._generate_test_task_list(task_list_id)
        self.assertEqual(task_list_id, task_list.id)

    def test_to_dict(self):
        task_list_id = 37617
        task_list = self._generate_test_task_list(task_list_id)
        task_dict = task_list.to_dict()
        self.assertEqual(task_list_id, task_dict["id"])
        self.assertIn(AC_PROPERTY_CLASS, task_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, task_dict.keys())

    def test_to_json(self):
        task_list_id = 37620
        task_list = self._generate_test_task_list(task_list_id)
        task_json = task_list.to_json()
        self.assertEqual(task_list_id, json.loads(task_json)["id"])
        self.assertIn(AC_PROPERTY_CLASS, json.loads(task_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(task_json).keys())
