import os.path
import time
from unittest import TestCase

from AcFileStorageProjectLabel import AcFileStorageProjectLabel
from AcProjectLabel import project_label_from_json
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS

DATA_DIR = './data'
ACCOUNT_ID = 12345


class TestAcFileStorageProjectLabel(TestCase):

    @staticmethod
    def _generate_test_project_label(label_id: int) -> dict:
        return {
            "id": label_id,
            "class": "ProjectLabel",
            "url_path": "/projects/label/%d" % label_id,
            "name": "Test Project Label",
            "updated_on": int(time.time()),
            "color": "#ff00ff",
            "lighter_text_color": "#ffa0ff",
            "darker_text_color": "#a0a0a0",
            "is_default": True,
            "position": 1,
            "project_id": 56
        }

    def test_get_path(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageProjectLabel(DATA_DIR, account_id)
        self.assertGreater(len(storage.get_path()), 1)

    def test_reset(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageProjectLabel(DATA_DIR, account_id)
        storage.reset()
        self.assertFalse(os.path.isdir(storage.get_path()))

    def test_ensure_dirs(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageProjectLabel(DATA_DIR, account_id)
        storage.ensure_dirs()
        self.assertTrue(os.path.isdir(storage.get_path()))

    def test_get_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageProjectLabel(DATA_DIR, account_id)
        project = project_label_from_json(self._generate_test_project_label(1))
        filename = storage.get_filename(project)
        self.assertGreater(len(filename), 0)

    def test_get_full_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageProjectLabel(DATA_DIR, account_id)
        project = project_label_from_json(self._generate_test_project_label(2))
        filename = storage.get_filename(project)
        full_filename = storage.get_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_save(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageProjectLabel(DATA_DIR, account_id)
        storage.reset()
        storage.ensure_dirs()
        project = project_label_from_json(self._generate_test_project_label(3))
        full_filename = storage.save(project)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))
        # test catch the wrong class
        project2 = project_label_from_json(self._generate_test_project_label(30))
        project2.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(project2)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
