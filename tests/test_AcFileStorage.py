import json
import os.path
import re
import time
from tempfile import mkstemp
from unittest import TestCase

from AcAttachment import AcAttachment, attachment_from_json
from AcCompany import company_from_json, AcCompany
from AcProjectLabel import AcProjectLabel
from AcStorage.AcFileStorage import AcFileStorage
from AcTaskHistory import AcTaskHistory
from AcTaskLabel import AcTaskLabel
from AcTaskList import AcTaskList, task_list_from_json
from ActiveCollabAPI.AcComment import AcComment, comment_from_json
from ActiveCollabAPI.AcProject import AcProject, project_from_json
from ActiveCollabAPI.AcSubtask import AcSubtask, subtask_from_json
from ActiveCollabAPI.AcTask import AcTask, task_from_json
from ActiveCollabAPI.AcUser import user_from_json, AcUser

DATA_DIR = './data'


class TestAcFileStorage(TestCase):

    def test__010_reset(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        self.assertFalse(os.path.isdir(ac_storage.get_account_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_tasks_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_projects_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_users_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_subtasks_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_comments_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_attachments_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_project_label_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_task_label_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_company_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_task_lists_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_task_history_path()))

    def test_020_ensure_dirs(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        self.assertTrue(os.path.isdir(ac_storage.get_account_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_tasks_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_projects_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_users_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_subtasks_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_comments_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_attachments_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_project_label_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_task_label_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_company_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_task_lists_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_task_history_path()))

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
        account_id = 12341234
        task_id = 3456
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task = self._generate_test_task(task_id)
        filename = ac_storage.get_task_filename(test_task)
        self.assertGreater(len(filename), 0)

    def test_120_get_task_full_filename(self):
        account_id = 12341234
        task_id = 3456
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task = self._generate_test_task(task_id)
        filename = ac_storage.get_task_filename(test_task)
        full_filename = ac_storage.get_task_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_130_save_task(self):
        account_id = 12341234
        task_id = 3456
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        test_task = self._generate_test_task(task_id)
        full_filename = ac_storage.save_task(test_task)
        self.assertTrue(os.path.isfile(full_filename))

    # task history

    def test_140_get_task_history_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        path = ac_storage.get_task_history_path()
        self.assertRegex(path, r'^.*\/account-' + str(account_id + 0) + r'\/task-history')
        self.assertTrue(os.path.isdir(path))

    def _generate_test_task_history(self, timestamp: int, task_id: int = None) -> AcTaskHistory:
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

    def test_150_get_task_history_filename(self):
        account_id = 12341234
        task_id = 56712
        timestamp = int(time.time())
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task_history = self._generate_test_task_history(timestamp, task_id)
        filename = ac_storage.get_task_history_filename(test_task_history)
        self.assertGreater(len(filename), 0)
        self.assertRegex(filename, r'task-history-%08d-%010d\.json$' % (task_id, timestamp))

    def test_160_get_task_history_full_filename(self):
        account_id = 12341234
        task_id = 56712
        timestamp = int(time.time())
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task_history = self._generate_test_task_history(timestamp, task_id)
        filename = ac_storage.get_task_history_filename(test_task_history)
        full_filename = ac_storage.get_task_history_full_filename(filename)
        self.assertGreater(len(full_filename), 0)
        self.assertRegex(full_filename,
                         r'^.*\/account-%08d\/task-history\/task-history-%08d-%010d\.json$' %
                         (account_id, task_id, timestamp))

    def test_170_save_task_history(self):
        account_id = 12341234
        timestamp = int(time.time())
        task_id = 56712
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.ensure_dirs()
        test_task_history = self._generate_test_task_history(timestamp, task_id)
        full_filename = ac_storage.save_task_history(test_task_history)
        self.assertGreater(len(full_filename), 0)
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
        account_id = 12341234
        project_id = 4321
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_project = self._generate_test_project(project_id)
        filename = ac_storage.get_project_filename(test_project)
        self.assertGreater(len(filename), 0)

    def test_220_get_project_full_filename(self):
        account_id = 12341234
        project_id = 4321
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_project = self._generate_test_project(project_id)
        filename = ac_storage.get_project_filename(test_project)
        full_filename = ac_storage.get_project_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_230_save_project(self):
        account_id = 12341234
        project_id = 4321
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
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
        account_id = 12341234
        user_id = 4711
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_user = self._generate_test_user(user_id)
        filename = ac_storage.get_user_filename(test_user)
        self.assertGreater(len(filename), 0)

    def test_320_get_user_full_filename(self):
        account_id = 12341234
        user_id = 4712
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_user = self._generate_test_user(user_id)
        filename = ac_storage.get_user_filename(test_user)
        full_filename = ac_storage.get_user_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_330_save_user(self):
        account_id = 12341234
        user_id = 4323
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
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

    def test_400_get_subtasks_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_subtasks_path()))

    def test_410_get_subtask_filename(self):
        account_id = 12341234
        task_id = 3456
        subtask_id = 987
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        subtest_task = self._generate_test_subtask(task_id, subtask_id)
        filename = ac_storage.get_subtask_filename(subtest_task)
        self.assertGreater(len(filename), 0)

    def test_420_get_subtask_full_filename(self):
        account_id = 12341234
        task_id = 3456
        subtask_id = 987
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        subtest_task = self._generate_test_subtask(task_id, subtask_id)
        filename = ac_storage.get_subtask_filename(subtest_task)
        full_filename = ac_storage.get_subtask_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_430_save_subtask(self):
        account_id = 12341234
        task_id = 3456
        subtask_id = 987
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        subtest_task = self._generate_test_subtask(task_id, subtask_id)
        full_filename = ac_storage.save_subtask(subtest_task)
        self.assertTrue(os.path.isfile(full_filename))

    # comments
    def _generate_test_comment(self, task_id: int, comment_id: int) -> AcComment:
        with open('../example-data/example-comment-95993.json', 'r') as fh:
            comment = comment_from_json(json.load(fh))
        comment.parent_id = task_id
        comment.id = comment_id
        return comment

    def test_500_get_comments_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        self.assertRegex(ac_storage.get_comments_path(), r'^.*\/account-' + str(account_id + 0) + r'\/comments$')
        self.assertTrue(os.path.isdir(ac_storage.get_comments_path()))

    def test_510_get_comment_filename(self):
        account_id = 12341234
        task_id = 3456
        comment_id = 667788
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_comment = self._generate_test_comment(task_id, comment_id)
        filename = ac_storage.get_comment_filename(test_comment)
        self.assertGreater(len(filename), 0)
        self.assertRegex(filename, r'^comment-%08d\.json$' % comment_id)

    def test_520_get_comment_full_filename(self):
        account_id = 12341234
        task_id = 3456
        comment_id = 987
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_comment = self._generate_test_comment(task_id, comment_id)
        filename = ac_storage.get_comment_filename(test_comment)
        full_filename = ac_storage.get_comment_full_filename(filename)
        self.assertGreater(len(full_filename), 0)
        self.assertRegex(full_filename, r'^.*\/account-%08d\/comments\/comment-%08d\.json$' % (account_id, comment_id))

    def test_530_save_comment(self):
        account_id = 12341234
        task_id = 3456
        comment_id = 987
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        test_comment = self._generate_test_comment(task_id, comment_id)
        full_filename = ac_storage.save_comment(test_comment)
        self.assertTrue(os.path.isfile(full_filename))

    # attachments
    def _generate_test_attachment(self, attachment_id: int) -> AcAttachment:
        with open('../example-data/example-attachment-29703.json', 'r') as fh:
            attachment = attachment_from_json(json.load(fh))
        attachment.id = attachment_id
        return attachment

    def test_600_get_attachments_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        path = ac_storage.get_attachments_path()
        self.assertRegex(path, r'^.*\/account-' + str(account_id + 0) + r'\/attachments$')
        self.assertTrue(os.path.isdir(path))

    def test_610_get_attachment_filename(self):
        account_id = 12341234
        attachment_id = 343421
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_attachment = self._generate_test_attachment(attachment_id)
        filename = ac_storage.get_attachment_filename(test_attachment)
        self.assertGreater(len(filename), 0)
        self.assertRegex(filename, r'^attachment-%08d\.json$' % attachment_id)

    def test_620_get_attachemnt_full_filename(self):
        account_id = 12341234
        attachment_id = 343421
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_attachment = self._generate_test_attachment(attachment_id)
        filename = ac_storage.get_attachment_filename(test_attachment)
        full_filename = ac_storage.get_attachment_full_filename(filename)
        self.assertGreater(len(full_filename), 0)
        self.assertRegex(full_filename,
                         r'^.*\/account-%08d\/attachments\/attachment-%08d\.json$' % (account_id, attachment_id))

    def test_630_save_attachment(self):
        account_id = 12341234
        attachment_id = 343421
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        test_attachment = self._generate_test_attachment(attachment_id)
        tmp_filename = mkstemp()[1]
        full_filename = ac_storage.save_attachment(test_attachment, tmp_filename)
        self.assertTrue(os.path.isfile(full_filename))

    # project labels

    def test_700_get_project_labels_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        path = ac_storage.get_project_label_path()
        self.assertRegex(path, r'^.*\/account-' + str(account_id + 0) + r'\/project-label')
        self.assertTrue(os.path.isdir(path))

    def _generate_test_project_label(self, label_id):
        return AcProjectLabel(
            id=label_id,
            class_="ProjectLabel",
            url_path="/project-label/%d" % label_id,
            name="Test Label",
            updated_on=123,
            color="#f02",
            lighter_text_color="#ffffff",
            darker_text_color="#000000",
            is_default=False,
            position=1,
            project_id=1234
        )

    def test_710_get_project_label_filename(self):
        account_id = 12341234
        project_label_id = 23
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_project_label = self._generate_test_project_label(project_label_id)
        project_label_filename = ac_storage.get_project_label_filename(test_project_label)
        self.assertGreater(len(project_label_filename), 0)
        self.assertRegex(project_label_filename, r'project-label-%08d\.json$' % project_label_id)

    def test_720_get_project_label_full_filename(self):
        account_id = 12341234
        project_label_id = 23
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_project_label = self._generate_test_project_label(project_label_id)
        project_label_filename = ac_storage.get_project_label_filename(test_project_label)
        full_filename = ac_storage.get_project_label_full_filename(project_label_filename)
        self.assertGreater(len(full_filename), 0)
        self.assertRegex(full_filename,
                         r'^.*\/account-%08d\/project-labels\/project-label-%08d\.json$' % (
                             account_id, project_label_id))

    def test_730_save_project_label(self):
        account_id = 12341234
        project_label_id = 23
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_project_label = self._generate_test_project_label(project_label_id)
        full_filename = ac_storage.save_project_label(test_project_label)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))

    # task labels

    def test_740_get_task_labels_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        path = ac_storage.get_task_label_path()
        self.assertRegex(path, r'^.*\/account-' + str(account_id + 0) + r'\/task-labels')
        self.assertTrue(os.path.isdir(path))

    def _generate_test_task_label(self, label_id):
        return AcTaskLabel(
            id=label_id,
            class_="TaskLabel",
            url_path="/task-label/%d" % label_id,
            name="Test Task Label",
            updated_on=123,
            color="#f02",
            lighter_text_color="#ffffff",
            darker_text_color="#000000",
            is_default=False,
            is_global=True,
            position=1,
            project_id=1234
        )

    def test_750_get_task_label_filename(self):
        account_id = 12341234
        task_label_id = 230
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task_label = self._generate_test_task_label(task_label_id)
        filename = ac_storage.get_task_label_filename(test_task_label)
        self.assertGreater(len(filename), 0)
        self.assertRegex(filename, r'task-label-%08d\.json$' % task_label_id)

    def test_760_get_task_label_full_filename(self):
        account_id = 12341234
        task_label_id = 237
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task_label = self._generate_test_task_label(task_label_id)
        filename = ac_storage.get_task_label_filename(test_task_label)
        full_filename = ac_storage.get_task_label_full_filename(filename)
        self.assertGreater(len(full_filename), 0)
        self.assertRegex(full_filename,
                         r'^.*\/account-%08d\/task-labels\/task-label-%08d\.json$' % (
                             account_id, task_label_id))

    def test_770_save_task_label(self):
        account_id = 12341234
        task_label_id = 238
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task_label = self._generate_test_task_label(task_label_id)
        full_filename = ac_storage.save_task_label(test_task_label)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))

    # companies

    def _generate_test_company(self, company_id: int) -> AcCompany:
        with open('../example-data/example-company-5.json', 'r') as fh:
            company = company_from_json(json.load(fh))
        company.id = company_id
        return company

    def test_800_get_companies_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        path = ac_storage.get_company_path()
        self.assertRegex(path, r'^.*\/account-' + str(account_id + 0) + r'\/companies')
        self.assertTrue(os.path.isdir(path))

    def test_810_get_company_filename(self):
        account_id = 12341234
        company_id = 8
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_company = self._generate_test_company(company_id)
        filename = ac_storage.get_company_filename(test_company)
        self.assertGreater(len(filename), 0)
        self.assertRegex(filename, r'company-%08d\.json$' % company_id)

    def test_820_get_company_full_filename(self):
        account_id = 12341234
        company_id = 9
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_company = self._generate_test_company(company_id)
        filename = ac_storage.get_company_filename(test_company)
        full_filename = ac_storage.get_company_full_filename(filename)
        self.assertGreater(len(full_filename), 0)
        self.assertRegex(full_filename,
                         r'^.*\/account-%08d\/companies\/company-%08d\.json$' % (
                             account_id, company_id))

    def test_830_save_company(self):
        account_id = 12341234
        company_id = 4
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        test_company = self._generate_test_company(company_id)
        full_filename = ac_storage.save_company(test_company)
        self.assertTrue(os.path.isfile(full_filename))

    # task lists

    def test_940_get_task_lists_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        path = ac_storage.get_task_lists_path()
        self.assertRegex(path, r'^.*\/account-' + str(account_id + 0) + r'\/task-lists')
        self.assertTrue(os.path.isdir(path))

    def _generate_test_task_list(self, task_list_id: int) -> AcTaskList:
        with open('../example-data/example-task-list-37314.json', 'r') as fh:
            task_list = task_list_from_json(json.load(fh))
        task_list.id = task_list_id
        return task_list

    def test_950_get_task_list_filename(self):
        account_id = 12341234
        task_list_id = 230
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task_list = self._generate_test_task_list(task_list_id)
        filename = ac_storage.get_task_list_filename(test_task_list)
        self.assertGreater(len(filename), 0)
        self.assertRegex(filename, r'task-list-%08d\.json$' % task_list_id)

    def test_960_get_task_list_full_filename(self):
        account_id = 12341234
        task_list_id = 237
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task_list = self._generate_test_task_list(task_list_id)
        filename = ac_storage.get_task_list_filename(test_task_list)
        full_filename = ac_storage.get_task_list_full_filename(filename)
        self.assertGreater(len(full_filename), 0)
        self.assertRegex(full_filename,
                         r'^.*\/account-%08d\/task-lists\/task-list-%08d\.json$' % (
                             account_id, task_list_id))

    def test_970_save_task_list(self):
        account_id = 12341234
        task_list_id = 238
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        test_task_list = self._generate_test_task_list(task_list_id)
        full_filename = ac_storage.save_task_list(test_task_list)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))
