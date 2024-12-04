import json
import os.path
from tempfile import mkstemp
from unittest import TestCase

from active_collab_api.AcAttachment import attachment_from_json
from active_collab_storage.AcFileStorageAttachment import AcFileStorageAttachment
from active_collab_api import AC_ERROR_WRONG_CLASS

DATA_DIR = "./data"
ACCOUNT_ID = 12345


class TestAcFileStorageAttachment(TestCase):
    @staticmethod
    def _generate_test_attachment(attachment_id: int) -> dict:
        with open("tests/example-data/example-attachment-29703.json", "r") as fh:
            attachment = json.load(fh)
        attachment["id"] = attachment_id
        return attachment

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

    def test_save_wrong_class(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageAttachment(DATA_DIR, account_id)
        storage.reset()
        storage.ensure_dirs()
        task = attachment_from_json(self._generate_test_attachment(58))
        task.class_ = "dummy"
        tmp_filename = mkstemp()[1]
        with self.assertRaises(AssertionError) as cm:
            storage.save(task, tmp_filename)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
