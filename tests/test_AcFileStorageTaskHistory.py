import os.path
import time
from unittest import TestCase

from AcFileStorageTaskHistory import AcFileStorageTaskHistory
from AcTaskHistory import task_history_from_json

DATA_DIR = './data'
ACCOUNT_ID = 12345


class TestAcFileStorageTaskHistory(TestCase):

    @staticmethod
    def _generate_test_task_history(timestamp: int, task_id: int = None) -> dict:
        return {
            "timestamp": timestamp,
            "created_by_id": 12,
            "created_by_name": 'Tester',
            "created_by_email": 'ac-api-test@example.com',
            "task_id": task_id,
            "modifications": [{
                "due_on": [
                    "2024-08-13",
                    "2024-08-20",
                    "Due date changed from <b>13. Aug 2024</b> to <b>20. Aug 2024</b>"
                ],
                "start_on":
                    [
                        "2024-08-13",
                        "2024-08-20",
                        "Start date changed from <b>13. Aug 2024</b> to <b>20. Aug 2024</b>"
                    ]
            }]
        }

    def test_get_path(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTaskHistory(DATA_DIR, account_id)
        self.assertGreater(len(storage.get_path()), 1)

    def test_reset(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTaskHistory(DATA_DIR, account_id)
        storage.reset()
        self.assertFalse(os.path.isdir(storage.get_path()))

    def test_ensure_dirs(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTaskHistory(DATA_DIR, account_id)
        storage.ensure_dirs()
        self.assertTrue(os.path.isdir(storage.get_path()))

    def test_get_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTaskHistory(DATA_DIR, account_id)
        t = int(time.time())
        task_id = 78
        task_history = task_history_from_json(self._generate_test_task_history(t, task_id))
        filename = storage.get_filename(task_history)
        self.assertGreater(len(filename), 0)

    def test_get_full_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTaskHistory(DATA_DIR, account_id)
        t = int(time.time())
        task_id = 79
        task_history = task_history_from_json(self._generate_test_task_history(t, task_id))
        filename = storage.get_filename(task_history)
        full_filename = storage.get_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_save(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageTaskHistory(DATA_DIR, account_id)
        storage.reset()
        storage.ensure_dirs()
        t = int(time.time())
        task_id = 79
        task_history = task_history_from_json(self._generate_test_task_history(t, task_id))
        full_filename = storage.save(task_history)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))
