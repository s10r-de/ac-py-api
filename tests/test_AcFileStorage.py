import json
import os.path
import re
from unittest import TestCase

from AcStorage.AcFileStorage import AcFileStorage


class TestAcFileStorage(TestCase):
    def test__010_reset(self):
        account_id = 12341234
        ac_storage = AcFileStorage('./data', account_id)
        ac_storage.reset()
        self.assertFalse(os.path.isdir(ac_storage.get_account_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_projects_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_tasks_path()))

    def test_020_ensure_dirs(self):
        account_id = 12341234
        ac_storage = AcFileStorage('./data', account_id)
        ac_storage.ensure_dirs()
        self.assertTrue(os.path.isdir(ac_storage.get_account_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_projects_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_tasks_path()))

    def test_030_get_account_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage('./data', account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_account_path()))

    def test_040_get_projects_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage('./data', account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_projects_path()))

    def test_050_get_tasks_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage('./data', account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_tasks_path()))

    def test_060_get_project_filename(self):
        account_id = 123412
        project_id = 45
        ac_storage = AcFileStorage('./data', account_id)
        test_project = json.loads('''
        {
            "id": %d,
            "title": "test dummy project",
            "class_": "Project"
        }
         ''' % (project_id))
        filename = ac_storage.get_project_filename(test_project)
        self.assertIsNotNone(filename.find(str(project_id)))

    def test__065_get_project_full_filename(self):
        account_id = 123412
        project_id = 45
        ac_storage = AcFileStorage('./data', account_id)
        test_project = json.loads('''
        {
            "id": %d,
            "title": "test dummy project",
            "class_": "Project"
        }
         ''' % (project_id))
        filename = ac_storage.get_project_filename(test_project)
        full_filename = ac_storage.get_project_full_filename(filename)
        self.assertIsNotNone(filename.find(str(project_id)))

    def test_070_save_project(self):
        account_id = 12341234
        project_id = 45
        ac_storage = AcFileStorage('./data', account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        test_project = json.loads('''
        {
            "id": %d,
            "title": "test dummy project",
            "class_": "Project"
        }
         ''' % (project_id))
        filename = ac_storage.save_project(test_project)
        self.assertTrue(os.path.isfile(filename))

    def test_080_get_task_filename(self):
        account_id = 123412
        task_id = 3456
        ac_storage = AcFileStorage('./data', account_id)
        test_task = json.loads('''
        {
            "id": %d,
            "title": "test dummy task",
            "class_": "Task"
        }
         ''' % (task_id))
        filename = ac_storage.get_task_filename(test_task)
        self.assertIsNotNone(filename.find(str(task_id)))

    def test_085_get_task_full_filename(self):
        account_id = 123412
        task_id = 3456
        ac_storage = AcFileStorage('./data', account_id)
        test_task = json.loads('''
        {
            "id": %d,
            "title": "test dummy task",
            "class_": "Task"
        }
         ''' % (task_id))
        filename = ac_storage.get_task_filename(test_task)
        full_filename = ac_storage.get_task_full_filename(filename)
        self.assertIsNotNone(full_filename.find(str(task_id)))

    def test_090_save_task(self):
        account_id = 123412
        task_id = 3456
        ac_storage = AcFileStorage('./data', account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        test_task = json.loads('''
        {
            "id": %d,
            "title": "test dummy task",
            "class_": "Task"
        }
         ''' % (task_id))
        full_filename = ac_storage.save_task(test_task)
        self.assertTrue(os.path.isfile(full_filename))
