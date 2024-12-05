import inspect
import json
import os.path
from unittest import TestCase

from active_collab_api import AC_ERROR_WRONG_CLASS
from active_collab_api.ac_project_category import project_category_from_json
from active_collab_storage.project_category import (
    AcFileStorageProjectCategory,
)

DATA_DIR = f"./data-test/{__name__}/"
ACCOUNT_ID = 12345


class TestProjectCategory(TestCase):
    @staticmethod
    def _generate_test_project_category(project_id: int) -> dict:
        with open(
            "tests/example-data/example-project-category-2.json", "r", encoding="utf-8"
        ) as fh:
            project_category_json = json.load(fh)
        project_category_json["id"] = project_id
        return project_category_json

    def test_save(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageProjectCategory(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        project_category = project_category_from_json(
            self._generate_test_project_category(3)
        )
        full_filename = storage.save(project_category)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))

    def test_save_wrong_class(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageProjectCategory(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        project_category = project_category_from_json(
            self._generate_test_project_category(30)
        )
        project_category.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(project_category)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
