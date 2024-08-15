import os.path
import re
from unittest import TestCase

from AcStorage.AcFileStorage import AcFileStorage
from ActiveCollabAPI.AcProject import AcProject
from ActiveCollabAPI.AcTask import AcTask
from ActiveCollabAPI.AcTaskDependencies import AcTaskDependencies

DATA_DIR = './data'


class TestAcFileStorage(TestCase):

    @classmethod
    def tearDownClass(cls):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        #ac_storage.reset()

    def test__010_reset(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        self.assertFalse(os.path.isdir(ac_storage.get_account_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_tasks_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_projects_path()))

    def test_020_ensure_dirs(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.ensure_dirs()
        self.assertTrue(os.path.isdir(ac_storage.get_account_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_tasks_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_projects_path()))

    def test_030_get_account_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_account_path()))

    # tasks

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

    def test_100_get_tasks_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_tasks_path()))

    def test_110_get_task_filename(self):
        account_id = 123412
        task_id = 3456
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task = self._test_task(task_id)
        filename = ac_storage.get_task_filename(test_task)
        self.assertIsNotNone(filename.find(str(task_id)))

    def test_120_get_task_full_filename(self):
        account_id = 123412
        task_id = 3456
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task = self._test_task(task_id)
        filename = ac_storage.get_task_filename(test_task)
        full_filename = ac_storage.get_task_full_filename(filename)
        self.assertIsNotNone(full_filename.find(str(task_id)))

    def test_130_save_task(self):
        account_id = 123412
        task_id = 3456
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.ensure_dirs()
        test_task = self._test_task(task_id)
        full_filename = ac_storage.save_task(test_task)
        self.assertTrue(os.path.isfile(full_filename))

    # projects

    def _test_project(self, project_id):
        return AcProject(
            based_on_id=0,
            based_on_type=None,
            body="",
            body_formatted="",
            budget=0.0,
            budget_type="",
            budgeting_interval="",
            category_id=0,
            class_="Project",
            company_id=0,
            completed_by_id=0,
            completed_on=0,
            count_discussions=0,
            count_files=0,
            count_notes=0,
            count_tasks=0,
            created_by_email="",
            created_by_id=0,
            created_by_name="",
            created_on=0,
            currency_id=0,
            email="",
            file_size=0,
            id=project_id,
            is_billable=False,
            is_client_reporting_enabled=False,
            is_completed=False,
            is_estimate_visible_to_subcontractors=False,
            is_sample=False,
            is_tracking_enabled=False,
            is_trashed=False,
            label_id=0,
            last_activity_on=0,
            leader_id=0,
            members=[1, 2],
            members_can_change_billable=False,
            name="",
            project_number=0,
            show_task_estimates_to_clients=False,
            task_estimates_enabled=False,
            trashed_by_id=0,
            trashed_on=False,
            updated_by_id=0,
            updated_on=0,
            url_path=""
        )

    def test_200_get_projects_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_projects_path()))

    def test_210_get_project_filename(self):
        account_id = 123412
        project_id = 4321
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_project = self._test_project(project_id)
        filename = ac_storage.get_project_filename(test_project)
        self.assertIsNotNone(filename.find(str(project_id)))

    def test_220_get_project_full_filename(self):
        account_id = 123412
        project_id = 4321
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_project = self._test_project(project_id)
        filename = ac_storage.get_project_filename(test_project)
        full_filename = ac_storage.get_project_full_filename(filename)
        self.assertIsNotNone(full_filename.find(str(project_id)))

    def test_230_save_project(self):
        account_id = 123412
        project_id = 4321
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.ensure_dirs()
        test_project = self._test_project(project_id)
        full_filename = ac_storage.save_project(test_project)
        self.assertTrue(os.path.isfile(full_filename))
