import json
from unittest import TestCase

from ActiveCollabAPI.AcProject import AcProject, project_from_json


class TestAcProject(TestCase):

    def _generate_test_project(self, project_id: int) -> AcProject:
        with open('../example-data/example-project-611.json', 'r') as fh:
            project = project_from_json(json.load(fh))
        project.id = project_id
        return project

    def test_constructor(self):
        project_id = 611
        project = self._generate_test_project(project_id)
        self.assertEqual(project.id, project_id)

    def test_to_dict(self):
        project_id = 611
        project = self._generate_test_project(project_id)
        project_dict = project.to_dict()
        self.assertEqual(project_dict["id"], project_id)

    def test_to_json(self):
        project_id = 611
        project = self._generate_test_project(project_id)
        project_json = project.to_json()
        self.assertEqual(json.loads(project_json)["id"], project_id)
