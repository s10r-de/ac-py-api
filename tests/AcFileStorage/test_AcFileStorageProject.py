import inspect
import json
import os.path
from unittest import TestCase

from AcStorage.AcFileStorageProject import AcFileStorageProject
from active_collab_api.AcProject import project_from_json
from active_collab_api import AC_ERROR_WRONG_CLASS

DATA_DIR = "./data-test/%s/" % __name__
ACCOUNT_ID = 12345


class TestAcFileStorageProject(TestCase):
    @staticmethod
    def _generate_test_project(project_id: int) -> dict:
        with open("tests/example-data/example-project-611.json", "r") as fh:
            project_son = json.load(fh)
        project_son["id"] = project_id
        return project_son

    def test_save(self):
        m_name = inspect.stack()[0][3]
        account_id = ACCOUNT_ID
        storage = AcFileStorageProject(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        project = project_from_json(self._generate_test_project(36))
        full_filename = storage.save(project)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))

    def test_save_wrong_class(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageProject(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        project = project_from_json(self._generate_test_project(360))
        project.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(project)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
