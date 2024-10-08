import json
import os.path
from tempfile import mkstemp
from unittest import TestCase

from AcAttachment import attachment_from_json
from AcFileStorageAttachment import AcFileStorageAttachment
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS

DATA_DIR = './data'
ACCOUNT_ID = 12345


class TestAcFileStorageAttachment(TestCase):

    @staticmethod
    def _generate_test_attachment(attachment_id: int) -> dict:
        with open('../example-data/example-attachment-29703.json', 'r') as fh:
            attachment = json.load(fh)
        attachment["id"] = attachment_id
        return attachment

    def test_get_path(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageAttachment(DATA_DIR, account_id)
        self.assertGreater(len(storage.get_path()), 1)

    def test_reset(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageAttachment(DATA_DIR, account_id)
        storage.reset()
        self.assertFalse(os.path.isdir(storage.get_path()))

    def test_ensure_dirs(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageAttachment(DATA_DIR, account_id)
        storage.ensure_dirs()
        self.assertTrue(os.path.isdir(storage.get_path()))

    def test_get_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageAttachment(DATA_DIR, account_id)
        task = attachment_from_json(self._generate_test_attachment(55))
        filename = storage.get_filename(task)
        self.assertGreater(len(filename), 0)

    def test_get_full_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageAttachment(DATA_DIR, account_id)
        task = attachment_from_json(self._generate_test_attachment(56))
        filename = storage.get_filename(task)
        full_filename = storage.get_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_save(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageAttachment(DATA_DIR, account_id)
        storage.reset()
        storage.ensure_dirs()
        task = attachment_from_json(self._generate_test_attachment(57))
        tmp_filename = mkstemp()[1]
        full_filename = storage.save(task, tmp_filename)
        # FIXME test attachment
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))
        # test catch the wrong class
        task2 = attachment_from_json(self._generate_test_attachment(58))
        task2.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(task2, tmp_filename)
        # FIXME assert tmp file not existing
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
