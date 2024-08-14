import os.path
import re
from unittest import TestCase

from AcStorage.AcFileStorage import AcFileStorage
from ActiveCollabAPI.AcTask import AcTask
from ActiveCollabAPI.AcTaskDependencies import AcTaskDependencies


class TestAcFileStorage(TestCase):
    def test__010_reset(self):
        account_id = 12341234
        ac_storage = AcFileStorage('./data', account_id)
        ac_storage.reset()
        self.assertFalse(os.path.isdir(ac_storage.get_account_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_tasks_path()))

    def test_020_ensure_dirs(self):
        account_id = 12341234
        ac_storage = AcFileStorage('./data', account_id)
        ac_storage.ensure_dirs()
        self.assertTrue(os.path.isdir(ac_storage.get_account_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_tasks_path()))

    def test_030_get_account_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage('./data', account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_account_path()))

    def test_050_get_tasks_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage('./data', account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_tasks_path()))

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

    def test_080_get_task_filename(self):
        account_id = 123412
        task_id = 3456
        ac_storage = AcFileStorage('./data', account_id)
        test_task = self._test_task(task_id)
        filename = ac_storage.get_task_filename(test_task)
        self.assertIsNotNone(filename.find(str(task_id)))

    def test_085_get_task_full_filename(self):
        account_id = 123412
        task_id = 3456
        ac_storage = AcFileStorage('./data', account_id)
        test_task = self._test_task(task_id)
        filename = ac_storage.get_task_filename(test_task)
        full_filename = ac_storage.get_task_full_filename(filename)
        self.assertIsNotNone(full_filename.find(str(task_id)))

    def test_090_save_task(self):
        account_id = 123412
        task_id = 3456
        ac_storage = AcFileStorage('./data', account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        test_task = self._test_task(task_id)
        full_filename = ac_storage.save_task(test_task)
        self.assertTrue(os.path.isfile(full_filename))
