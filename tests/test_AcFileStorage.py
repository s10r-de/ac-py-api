import json
import os.path
import re
from unittest import TestCase

from AcStorage.AcFileStorage import AcFileStorage
from ActiveCollabAPI.AcProject import AcProject, project_from_json
from ActiveCollabAPI.AcSubtask import AcSubtask, subtask_from_json
from ActiveCollabAPI.AcTask import AcTask, task_from_json
from ActiveCollabAPI.AcUser import user_from_json, AcUser

DATA_DIR = './data'


class TestAcFileStorage(TestCase):

    @classmethod
    def tearDownClass(cls):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        # ac_storage.reset()

    def test__010_reset(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        self.assertFalse(os.path.isdir(ac_storage.get_account_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_tasks_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_projects_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_users_path()))

    def test_020_ensure_dirs(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.ensure_dirs()
        self.assertTrue(os.path.isdir(ac_storage.get_account_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_tasks_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_projects_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_users_path()))

    def test_030_get_account_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_account_path()))

    # tasks
    def _generate_test_task(self, task_id: int) -> AcTask:
        with open('../example-data/example-task-17614.json', 'r') as fh:
            task = task_from_json(json.load(fh))
        task.id = task_id
        return task

    def test_100_get_tasks_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_tasks_path()))

    def test_110_get_task_filename(self):
        account_id = 123412
        task_id = 3456
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task = self._generate_test_task(task_id)
        filename = ac_storage.get_task_filename(test_task)
        self.assertGreater(len(filename), 0)

    def test_120_get_task_full_filename(self):
        account_id = 123412
        task_id = 3456
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task = self._generate_test_task(task_id)
        filename = ac_storage.get_task_filename(test_task)
        full_filename = ac_storage.get_task_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_130_save_task(self):
        account_id = 123412
        task_id = 3456
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.ensure_dirs()
        test_task = self._generate_test_task(task_id)
        full_filename = ac_storage.save_task(test_task)
        self.assertTrue(os.path.isfile(full_filename))

    # projects

    def _generate_test_project(self, project_id: int) -> AcProject:
        with open('../example-data/example-project-611.json', 'r') as fh:
            project = project_from_json(json.load(fh))
        project.id = project_id
        return project

    def test_200_get_projects_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_projects_path()))

    def test_210_get_project_filename(self):
        account_id = 123412
        project_id = 4321
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_project = self._generate_test_project(project_id)
        filename = ac_storage.get_project_filename(test_project)
        self.assertGreater(len(filename), 0)

    def test_220_get_project_full_filename(self):
        account_id = 123412
        project_id = 4321
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_project = self._generate_test_project(project_id)
        filename = ac_storage.get_project_filename(test_project)
        full_filename = ac_storage.get_project_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_230_save_project(self):
        account_id = 123412
        project_id = 4321
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.ensure_dirs()
        test_project = self._generate_test_project(project_id)
        full_filename = ac_storage.save_project(test_project)
        self.assertTrue(os.path.isfile(full_filename))

    # users

    def _generate_test_user(self, user_id: int) -> AcUser:
        with open('../example-data/example-user-00000240.json', 'r') as fh:
            user = user_from_json(json.load(fh))
        user.id = user_id
        return user

    def test_300_get_users_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_users_path()))

    def test_310_get_user_filename(self):
        account_id = 123412
        user_id = 4711
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_user = self._generate_test_user(user_id)
        filename = ac_storage.get_user_filename(test_user)
        self.assertGreater(len(filename), 0)

    def test_320_get_user_full_filename(self):
        account_id = 123412
        user_id = 4712
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_user = self._generate_test_user(user_id)
        filename = ac_storage.get_user_filename(test_user)
        full_filename = ac_storage.get_user_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_330_save_user(self):
        account_id = 123412
        user_id = 4323
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.ensure_dirs()
        test_user = self._generate_test_user(user_id)
        full_filename = ac_storage.save_user(test_user)
        self.assertTrue(os.path.isfile(full_filename))

    # subtasks
    def _generate_test_subtask(self, task_id: int, subtask_id: int) -> AcSubtask:
        with open('../example-data/example-subtask-00041071.json', 'r') as fh:
            subtask = subtask_from_json(json.load(fh))
        subtask.task_id = task_id
        subtask.id = subtask_id
        return subtask

    def test_400_get_tasks_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_subtasks_path()))

    def test_410_get_subtask_filename(self):
        account_id = 123412
        task_id = 3456
        subtask_id = 987
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        subtest_task = self._generate_test_subtask(task_id, subtask_id)
        filename = ac_storage.get_subtask_filename(subtest_task)
        self.assertGreater(len(filename), 0)

    def test_420_get_subtask_full_filename(self):
        account_id = 123412
        task_id = 3456
        subtask_id = 987
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        subtest_task = self._generate_test_subtask(task_id, subtask_id)
        filename = ac_storage.get_subtask_filename(subtest_task)
        full_filename = ac_storage.get_subtask_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_430_save_subtask(self):
        account_id = 123412
        task_id = 3456
        subtask_id = 987
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.ensure_dirs()
        subtest_task = self._generate_test_subtask(task_id, subtask_id)
        full_filename = ac_storage.save_subtask(subtest_task)
        self.assertTrue(os.path.isfile(full_filename))
