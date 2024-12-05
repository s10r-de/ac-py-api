import inspect
import json
import os.path
from unittest import TestCase

from active_collab_api import AC_ERROR_WRONG_CLASS
from active_collab_api.ac_task import task_from_json
from active_collab_storage.task import AcFileStorageTask

DATA_DIR = f"./data-test/{__name__}/"
ACCOUNT_ID = 12345


class TestTask(TestCase):
    @staticmethod
    def _generate_test_task(task_id: int) -> dict:
        with open(
            "tests/example-data/example-task-17614.json", "r", encoding="utf-8"
        ) as fh:
            task_json = json.load(fh)
        task_json["id"] = task_id
        return task_json

    def test_save(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageTask(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        task = task_from_json(self._generate_test_task(36))
        full_filename = storage.save(task)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))

    def test_save_wrong_class(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageTask(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        task2 = task_from_json(self._generate_test_task(360))
        task2.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(task2)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
