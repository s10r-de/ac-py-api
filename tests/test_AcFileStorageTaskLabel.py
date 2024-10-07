import os.path
import time
from unittest import TestCase

from AcFileStorageTaskLabel import AcFileStorageTaskLabel
from AcTaskLabel import task_label_from_json
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS

DATA_DIR = './data'
ACCOUNT_ID = 12345


class TestAcFileStorageTaskLabel(TestCase):

    @staticmethod
    def _generate_test_task_label(label_id: int) -> dict:
        return {
            "id": label_id,
            "class": "TaskLabel",
            "url_path": "/task/label/%d" % label_id,
            "name": "Test Task Label",
            "updated_on": int(time.time()),
            "color": "#ff00ff",
            "lighter_text_color": "#ffa0ff",
            "darker_text_color": "#a0a0a0",
            "is_default": True,
            "is_global": True,
            "position": 3,
            "project_id": 34
        }

    def test_get_path(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTaskLabel(DATA_DIR, account_id)
        self.assertGreater(len(storage.get_path()), 1)

    def test_reset(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTaskLabel(DATA_DIR, account_id)
        storage.reset()
        self.assertFalse(os.path.isdir(storage.get_path()))

    def test_ensure_dirs(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTaskLabel(DATA_DIR, account_id)
        storage.ensure_dirs()
        self.assertTrue(os.path.isdir(storage.get_path()))

    def test_get_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTaskLabel(DATA_DIR, account_id)
        task_label = task_label_from_json(self._generate_test_task_label(35))
        filename = storage.get_filename(task_label)
        self.assertGreater(len(filename), 0)

    def test_get_full_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTaskLabel(DATA_DIR, account_id)
        task_label = task_label_from_json(self._generate_test_task_label(34))
        filename = storage.get_filename(task_label)
        full_filename = storage.get_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_save(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTaskLabel(DATA_DIR, account_id)
        storage.reset()
        storage.ensure_dirs()
        task_label = task_label_from_json(self._generate_test_task_label(36))
        full_filename = storage.save(task_label)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))
        # test catch the wrong class
        task_label2 = task_label_from_json(self._generate_test_task_label(360))
        task_label2.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(task_label2)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
