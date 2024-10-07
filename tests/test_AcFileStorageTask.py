import json
import os.path
from unittest import TestCase

from AcFileStorageTask import AcFileStorageTask
from AcTask import task_from_json
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS

DATA_DIR = './data'
ACCOUNT_ID = 12345


class TestAcFileStorageTask(TestCase):

    @staticmethod
    def _generate_test_task(task_id: int) -> dict:
        with open('../example-data/example-task-17614.json', 'r') as fh:
            task_json = json.load(fh)
        task_json["id"] = task_id
        return task_json

    def test_get_path(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTask(DATA_DIR, account_id)
        self.assertGreater(len(storage.get_path()), 1)

    def test_reset(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTask(DATA_DIR, account_id)
        storage.reset()
        self.assertFalse(os.path.isdir(storage.get_path()))

    def test_ensure_dirs(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTask(DATA_DIR, account_id)
        storage.ensure_dirs()
        self.assertTrue(os.path.isdir(storage.get_path()))

    def test_get_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTask(DATA_DIR, account_id)
        task = task_from_json(self._generate_test_task(35))
        filename = storage.get_filename(task)
        self.assertGreater(len(filename), 0)

    def test_get_full_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTask(DATA_DIR, account_id)
        task = task_from_json(self._generate_test_task(34))
        filename = storage.get_filename(task)
        full_filename = storage.get_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_save(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTask(DATA_DIR, account_id)
        storage.reset()
        storage.ensure_dirs()
        task = task_from_json(self._generate_test_task(36))
        full_filename = storage.save(task)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))
        # test catch the wrong class
        task2 = task_from_json(self._generate_test_task(360))
        task2.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(task2)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
