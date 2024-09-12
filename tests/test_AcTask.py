import json
from unittest import TestCase

from AcTaskDependencies import AcTaskDependencies
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

    def test_to_dict_with_dependencies(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        task.open_dependencies = AcTaskDependencies(parents_count=2, children_count=3)
        task.attachments = None
        task_dict = task.to_dict()
        self.assertEqual(task_dict["id"], task_id)
        self.assertEqual(task_dict["open_dependencies"]["parents_count"], 2)
        self.assertEqual(task_dict["open_dependencies"]["children_count"], 3)

    def test_to_json_with_dependencies(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        task.open_dependencies = AcTaskDependencies(parents_count=2, children_count=3)
        task.attachments = None
        task_json = task.to_json()
        parsed_json = json.loads(task_json)
        self.assertEqual(parsed_json["id"], task_id)
        self.assertEqual(parsed_json["open_dependencies"]["parents_count"], 2)
        self.assertEqual(parsed_json["open_dependencies"]["children_count"], 3)
