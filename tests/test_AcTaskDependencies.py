import json
from unittest import TestCase

from active_collab_api.AcTaskDependencies import (
    AcTaskDependencies,
    taskdependency_from_json,
)


class TestAcTaskDependencies(TestCase):
    def test_to_dict(self):
        task_dependencies = AcTaskDependencies(parents_count=2, children_count=3)
        task_dependencies_dict = task_dependencies.to_dict()
        self.assertIsInstance(task_dependencies_dict, dict)
        self.assertEqual(2, task_dependencies.parents_count)
        self.assertEqual(3, task_dependencies.children_count)

    def test_to_json(self):
        task_dependencies = AcTaskDependencies(parents_count=2, children_count=3)
        task_dependencies_json = task_dependencies.to_json()
        self.assertIsInstance(task_dependencies_json, str)
        o = json.loads(task_dependencies_json)
        self.assertEqual(2, o["parents_count"])
        self.assertEqual(3, o["children_count"])

    def test_from_dict(self):
        task_dependency_json = """{
            "parents_count": 5,
            "children_count": 6
        }"""
        task_dependencies = taskdependency_from_json(json.loads(task_dependency_json))
        self.assertIsInstance(task_dependencies, AcTaskDependencies)
        self.assertEqual(5, task_dependencies.parents_count)
        self.assertEqual(6, task_dependencies.children_count)
