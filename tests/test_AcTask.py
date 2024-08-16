import json
from unittest import TestCase

from ActiveCollabAPI.AcTask import AcTask, task_from_json


class TestAcTask(TestCase):

    def _generate_test_task(self, task_id: int) -> AcTask:
        with open('../example-data/example-task-17614.json', 'r') as fh:
            task = task_from_json(json.load(fh))
        task.id = task_id
        return task

    def test_actask_constructor(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        self.assertEqual(task_id, task.id)

    def test_to_dict(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        task_dict = task.to_dict()
        self.assertEqual(task_dict["id"], task_id)

    def test_to_json(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        task_json = task.to_json()
        self.assertEqual(json.loads(task_json)["id"], task_id)
