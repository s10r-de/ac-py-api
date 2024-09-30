import json
from unittest import TestCase

from ActiveCollabAPI import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_
from ActiveCollabAPI.AcProject import AcProject, project_from_json


class TestAcProject(TestCase):

    @staticmethod
    def _generate_test_project(project_id: int) -> AcProject:
        with open('../example-data/example-project-611.json', 'r') as fh:
            project = project_from_json(json.load(fh))
        project.id = project_id
        return project

    def test_constructor(self):
        project_id = 611
        project = self._generate_test_project(project_id)
        self.assertEqual(project_id, project.id)

    def test_to_dict(self):
        project_id = 611
        project = self._generate_test_project(project_id)
        project_dict = project.to_dict()
        self.assertEqual(project_id, project_dict["id"])
        self.assertIn(AC_PROPERTY_CLASS, project_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, project_dict.keys())

    def test_to_json(self):
        project_id = 611
        project = self._generate_test_project(project_id)
        project_json = project.to_json()
        self.assertEqual(project_id, json.loads(project_json)["id"])
        self.assertIn(AC_PROPERTY_CLASS, json.loads(project_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(project_json).keys())
