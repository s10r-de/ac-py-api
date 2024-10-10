import json
import os.path
from unittest import TestCase

from AcFileStorageProjectCategory import AcFileStorageProjectCategory
from AcProjectCategory import project_category_from_json
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS

DATA_DIR = './data'
ACCOUNT_ID = 12345


class TestAcFileStorageProjectCategory(TestCase):

    @staticmethod
    def _generate_test_project_category(project_id: int) -> dict:
        with open('../example-data/example-project-category-2.json', 'r') as fh:
            project_category_json = json.load(fh)
        project_category_json["id"] = project_id
        return project_category_json

    def test_get_path(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageProjectCategory(DATA_DIR, account_id)
        self.assertGreater(len(storage.get_path()), 1)

    def test_reset(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageProjectCategory(DATA_DIR, account_id)
        storage.reset()
        self.assertFalse(os.path.isdir(storage.get_path()))

    def test_ensure_dirs(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageProjectCategory(DATA_DIR, account_id)
        storage.ensure_dirs()
        self.assertTrue(os.path.isdir(storage.get_path()))

    def test_get_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageProjectCategory(DATA_DIR, account_id)
        project = project_category_from_json(self._generate_test_project_category(1))
        filename = storage.get_filename(project)
        self.assertGreater(len(filename), 0)

    def test_get_full_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageProjectCategory(DATA_DIR, account_id)
        project = project_category_from_json(self._generate_test_project_category(2))
        filename = storage.get_filename(project)
        full_filename = storage.get_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_save(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageProjectCategory(DATA_DIR, account_id)
        storage.reset()
        storage.ensure_dirs()
        project = project_category_from_json(self._generate_test_project_category(3))
        full_filename = storage.save(project)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))
        # test catch the wrong class
        project2 = project_category_from_json(self._generate_test_project_category(30))
        project2.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(project2)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
