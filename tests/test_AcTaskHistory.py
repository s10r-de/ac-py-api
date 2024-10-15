import json
import time
from unittest import TestCase

from AcTaskHistory import AcTaskHistory, task_history_from_json


class TestAcTaskHistory(TestCase):

    @staticmethod
    def _generate_test_task_history(timestamp: int, task_id: int = None) -> AcTaskHistory:
        return AcTaskHistory(
            timestamp=timestamp,
            created_by_id=12,
            created_by_name='Tester',
            created_by_email='ac-api-test@example.com',
            task_id=task_id,
            modifications=[{
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
        )

    def test_constructor_without_task_id(self):
        timestamp = int(time.time())
        task_history = AcTaskHistory(
            timestamp=timestamp,
            created_by_id=12,
            created_by_name='Tester',
            created_by_email='ac-api-test@example.com',
            modifications=[{
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
        )
        self.assertEqual(timestamp, task_history.timestamp)
        self.assertEqual(0, task_history.task_id)

    def test_constructor_with_task_id(self):
        timestamp = int(time.time())
        task_id = 78
        task_history = AcTaskHistory(
            timestamp=timestamp,
            created_by_id=12,
            created_by_name='Tester',
            created_by_email='ac-api-test@example.com',
            task_id=task_id,
            modifications=[{
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
        )
        self.assertEqual(timestamp, task_history.timestamp)
        self.assertEqual(task_id, task_history.task_id)

    def test_to_dict(self):
        timestamp = int(time.time())
        task_id = 78
        task_history = self._generate_test_task_history(timestamp, task_id)
        task_history_dict = task_history.to_dict()
        self.assertEqual(task_id, task_history_dict["task_id"])
        self.assertEqual(timestamp, task_history_dict["timestamp"])

    def test_to_json(self):
        timestamp = int(time.time())
        task_id = 78
        task_history = self._generate_test_task_history(timestamp, task_id)
        task_history_json = task_history.to_json()
        self.assertEqual(task_id, json.loads(task_history_json)["task_id"])
        self.assertEqual(timestamp, json.loads(task_history_json)["timestamp"])

    def test_from_json(self):
        with open("example-data/example-task-history-1727425588.json", "r") as f:
            task_history_json = json.load(f)
        task_history = task_history_from_json(task_history_json, 8731)
        self.assertEqual(1727425588, task_history.timestamp)
        self.assertEqual(8731, task_history.task_id)
