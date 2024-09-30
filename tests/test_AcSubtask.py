import json
from unittest import TestCase

from ActiveCollabAPI import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_
from ActiveCollabAPI.AcSubtask import subtask_from_json, AcSubtask


class TestAcSubtask(TestCase):

    @staticmethod
    def _generate_test_subtask(task_id: int, subtask_id: int) -> AcSubtask:
        with open('../example-data/example-subtask-00041071.json', 'r') as fh:
            subtask = subtask_from_json(json.load(fh))
        subtask.task_id = task_id
        subtask.id = subtask_id
        return subtask

    def test_actask_constructor(self):
        task_id = 17614
        subtask_id = 70123
        subtask = self._generate_test_subtask(task_id, subtask_id)
        self.assertEqual(subtask_id, subtask.id)
        self.assertEqual(task_id, subtask.task_id)

    def test_to_dict(self):
        task_id = 17614
        subtask_id = 70123
        subtask = self._generate_test_subtask(task_id, subtask_id)
        subtask_dict = subtask.to_dict()
        self.assertEqual(subtask_id, subtask_dict["id"])
        self.assertEqual(task_id, subtask_dict["task_id"])
        self.assertIn(AC_PROPERTY_CLASS, subtask_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, subtask_dict.keys())

    def test_to_json(self):
        task_id = 17614
        subtask_id = 70123
        subtask = self._generate_test_subtask(task_id, subtask_id)
        subtask_json = subtask.to_json()
        self.assertEqual(subtask_id, json.loads(subtask_json)["id"])
        self.assertEqual(task_id, json.loads(subtask_json)["task_id"])
        self.assertIn(AC_PROPERTY_CLASS, json.loads(subtask_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(subtask_json).keys())
