import json
from unittest import TestCase

from AcTaskDependencies import AcTaskDependencies, taskdependency_from_json


class TestAcTaskDependencies(TestCase):

    def test_to_dict(self):
        task_dependencies = AcTaskDependencies(parents_count=2, children_count=3)
        task_dependencies_dict = task_dependencies.to_dict()
        self.assertIsInstance(task_dependencies_dict, dict)
        self.assertEqual(task_dependencies.parents_count, 2)
        self.assertEqual(task_dependencies.children_count, 3)

    def test_to_json(self):
        task_dependencies = AcTaskDependencies(parents_count=2, children_count=3)
        task_dependencies_json = task_dependencies.to_json()
        self.assertIsInstance(task_dependencies_json, str)
        o = json.loads(task_dependencies_json)
        self.assertEqual(o['parents_count'], 2)
        self.assertEqual(o['children_count'], 3)

    def test_from_dict(self):
        taskdependency_json = '''{
            "parents_count": 5,
            "children_count": 6
        }'''
        task_dependencies = taskdependency_from_json(json.loads(taskdependency_json))
        self.assertIsInstance(task_dependencies, AcTaskDependencies)
        self.assertEqual(task_dependencies.parents_count, 5)
        self.assertEqual(task_dependencies.children_count, 6)
