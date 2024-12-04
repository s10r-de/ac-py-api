import inspect
import json
import os.path
from unittest import TestCase

from active_collab_storage.AcFileStorageTaskList import AcFileStorageTaskList
from active_collab_api.AcTaskList import task_list_from_json
from active_collab_api import AC_ERROR_WRONG_CLASS

DATA_DIR = "./data-test/%s/" % __name__
ACCOUNT_ID = 12345


class TestAcFileStorageTaskList(TestCase):
    @staticmethod
    def _generate_test_task_list(task_list_id: int) -> dict:
        with open("tests/example-data/example-task-list-37314.json", "r") as fh:
            task_list_json = json.load(fh)
        task_list_json["id"] = task_list_id
        return task_list_json

    def test_save(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageTaskList(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        task_list = task_list_from_json(self._generate_test_task_list(36))
        full_filename = storage.save(task_list)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))

    def test_save_wrong_clas(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageTaskList(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        task_list = task_list_from_json(self._generate_test_task_list(360))
        task_list.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(task_list)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
