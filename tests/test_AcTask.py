import json
from unittest import TestCase

from ActiveCollabAPI.AcTask import AcTask
from ActiveCollabAPI.AcTaskDependencies import AcTaskDependencies


class TestAcTask(TestCase):
    def _test_task(self, task_id: int):
        return AcTask(
            assignee_id=0,
            attachments=[],
            body="test body",
            body_formatted="test body formatted",
            body_mode="",
            class_="Task",
            comments_count=0,
            completed_by_id=0,
            completed_on=0,
            completed_subtasks=0,
            created_by_email="",
            created_by_id=0,
            created_by_name="",
            created_from_recurring_task_id=0,
            created_on=0,
            delegated_by_id=0,
            due_on=0,
            estimate=0,
            fake_assignee_email="",
            fake_assignee_name="",
            id=task_id,
            is_billable=False,
            is_completed=False,
            is_hidden_from_clients=False,
            is_important=False,
            is_trashed=False,
            job_type_id=0,
            labels=[],
            name="Task Name",
            open_dependencies=AcTaskDependencies(
                parents_count=0,
                children_count=0
            ),
            open_subtasks=0,
            position=0,
            project_id=0,
            start_on=0,
            task_list_id=0,
            task_number=0,
            total_subtasks=0,
            trashed_by_id=0,
            trashed_on=0,
            updated_by_id=0,
            updated_on=0,
            url_path=""
        )

    def test_actask_constructor(self):
        task_id = 123456
        task = self._test_task(task_id)
        self.assertEqual(task_id, task.id)

    def test_to_dict(self):
        task_id = 123456
        task = self._test_task(task_id)
        task_dict = task.to_dict()
        self.assertEqual(task_id, task_dict["id"])

    def test_to_json(self):
        task_id = 123456
        task = self._test_task(task_id)
        task_json = task.to_json()
        self.assertEqual(task_id, json.loads(task_json)["id"])
