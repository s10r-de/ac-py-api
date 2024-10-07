import json
import os.path
import re
import time
from tempfile import mkstemp
from unittest import TestCase

from AcAttachment import AcAttachment, attachment_from_json
from AcStorage.AcFileStorage import AcFileStorage
from AcTaskHistory import AcTaskHistory
from ActiveCollabAPI.AcComment import AcComment, comment_from_json
from ActiveCollabAPI.AcSubtask import AcSubtask, subtask_from_json

DATA_DIR = './data'


class TestAcFileStorage(TestCase):

    def test__010_reset(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        self.assertFalse(os.path.isdir(ac_storage.get_account_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["tasks"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["projects"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["users"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_subtasks_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_comments_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_attachments_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["project-labels"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["task-labels"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["company"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["task-lists"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_task_history_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["project-categories"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["project-notes"].get_path()))

    def test_020_ensure_dirs(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        self.assertTrue(os.path.isdir(ac_storage.get_account_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["tasks"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["projects"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["users"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_subtasks_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_comments_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_attachments_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["project-labels"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["task-labels"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["company"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["task-lists"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_task_history_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["project-categories"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["project-notes"].get_path()))

    def test_030_get_account_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_account_path()))

    # task history

    def test_140_get_task_history_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        ac_storage.reset()
        ac_storage.ensure_dirs()
        path = ac_storage.get_task_history_path()
        self.assertRegex(path, r'^.*\/account-' + str(account_id + 0) + r'\/task-history')
        self.assertTrue(os.path.isdir(path))

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

    # subtasks
    @staticmethod
    def _generate_test_subtask(task_id: int, subtask_id: int) -> AcSubtask:
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
    @staticmethod
    def _generate_test_comment(task_id: int, comment_id: int) -> AcComment:
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
    @staticmethod
    def _generate_test_attachment(attachment_id: int) -> AcAttachment:
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

    def test_620_get_attachment_full_filename(self):
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
