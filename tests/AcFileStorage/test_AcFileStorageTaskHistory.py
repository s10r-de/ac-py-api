import inspect
import os.path
import time
from unittest import TestCase

from AcStorage.AcFileStorageTaskHistory import AcFileStorageTaskHistory
from active_collab_api.AcTaskHistory import task_history_from_json

DATA_DIR = "./data-test/%s/" % __name__
ACCOUNT_ID = 12345


class TestAcFileStorageTaskHistory(TestCase):
    @staticmethod
    def _generate_test_task_history(timestamp: int, task_id: int = None) -> dict:
        return {
            "timestamp": timestamp,
            "created_by_id": 12,
            "created_by_name": "Tester",
            "created_by_email": "ac-api-test@example.com",
            "modifications": [
                {
                    "due_on": [
                        "2024-08-13",
                        "2024-08-20",
                        "Due date changed from <b>13. Aug 2024</b> to <b>20. Aug 2024</b>",
                    ],
                    "start_on": [
                        "2024-08-13",
                        "2024-08-20",
                        "Start date changed from <b>13. Aug 2024</b> to <b>20. Aug 2024</b>",
                    ],
                }
            ],
        }

    def test_save(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageTaskHistory(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        t = int(time.time())
        task_id = 79
        task_history = task_history_from_json(
            self._generate_test_task_history(t), task_id
        )
        full_filename = storage.save(task_history)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))
