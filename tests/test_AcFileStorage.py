import json
import os.path
import re
from tempfile import mkstemp
from unittest import TestCase

from AcAttachment import AcAttachment, attachment_from_json
from AcStorage.AcFileStorage import AcFileStorage

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
        self.assertFalse(os.path.isdir(ac_storage.data_objects["subtasks"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["comments"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.get_attachments_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["project-labels"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["task-labels"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["company"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["task-lists"].get_path()))
        self.assertFalse(os.path.isdir(ac_storage.data_objects["task-history"].get_path()))
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
        self.assertTrue(os.path.isdir(ac_storage.data_objects["subtasks"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["comments"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.get_attachments_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["project-labels"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["task-labels"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["company"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["task-lists"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["task-history"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["project-categories"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["project-notes"].get_path()))

    def test_030_get_account_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_account_path()))

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
