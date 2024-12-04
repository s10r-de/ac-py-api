import inspect
import json
import os.path
from unittest import TestCase

from active_collab_api import AC_ERROR_WRONG_CLASS
from active_collab_api.ac_subtask import subtask_from_json
from active_collab_storage.subtask import AcFileStorageSubtask

DATA_DIR = "./data-test/%s/" % __name__
ACCOUNT_ID = 12345


class TestAcFileStorageSubtask(TestCase):
    @staticmethod
    def _generate_test_subtask(task_id: int, subtask_id: int) -> dict:
        with open("tests/example-data/example-subtask-00041071.json", "r") as fh:
            subtask = json.load(fh)
        subtask["task_id"] = task_id
        subtask["id"] = subtask_id
        return subtask

    def test_save(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageSubtask(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        task = subtask_from_json(self._generate_test_subtask(36, 6))
        full_filename = storage.save(task)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))

    def test_save_wrong_class(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageSubtask(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        task2 = subtask_from_json(self._generate_test_subtask(360, 7))
        task2.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(task2)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
