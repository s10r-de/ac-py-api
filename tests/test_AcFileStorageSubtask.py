import json
import os.path
from unittest import TestCase

from AcFileStorageSubtask import AcFileStorageSubtask
from AcSubtask import subtask_from_json
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS

DATA_DIR = './data'
ACCOUNT_ID = 12345


class TestAcFileStorageSubtask(TestCase):

    @staticmethod
    def _generate_test_subtask(task_id: int, subtask_id: int) -> dict:
        with open('../example-data/example-subtask-00041071.json', 'r') as fh:
            subtask = json.load(fh)
        subtask["task_id"] = task_id
        subtask["id"] = subtask_id
        return subtask

    def test_get_path(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageSubtask(DATA_DIR, account_id)
        self.assertGreater(len(storage.get_path()), 1)

    def test_reset(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageSubtask(DATA_DIR, account_id)
        storage.reset()
        self.assertFalse(os.path.isdir(storage.get_path()))

    def test_ensure_dirs(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageSubtask(DATA_DIR, account_id)
        storage.ensure_dirs()
        self.assertTrue(os.path.isdir(storage.get_path()))

    def test_get_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageSubtask(DATA_DIR, account_id)
        task = subtask_from_json(self._generate_test_subtask(35, 4))
        filename = storage.get_filename(task)
        self.assertGreater(len(filename), 0)

    def test_get_full_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageSubtask(DATA_DIR, account_id)
        task = subtask_from_json(self._generate_test_subtask(34, 5))
        filename = storage.get_filename(task)
        full_filename = storage.get_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_save(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageSubtask(DATA_DIR, account_id)
        storage.reset()
        storage.ensure_dirs()
        task = subtask_from_json(self._generate_test_subtask(36, 6))
        full_filename = storage.save(task)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))
        # test catch the wrong class
        task2 = subtask_from_json(self._generate_test_subtask(360, 7))
        task2.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(task2)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
