import json
import os.path
import re
from unittest import TestCase

from active_collab_api.ac_attachment import AcAttachment, attachment_from_json
from active_collab_storage.storage import AcFileStorage

DATA_DIR = "./data"


class TestStorage(TestCase):
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
        self.assertFalse(
            os.path.isdir(ac_storage.data_objects["attachments"].get_path())
        )
        self.assertFalse(
            os.path.isdir(ac_storage.data_objects["project-labels"].get_path())
        )
        self.assertFalse(
            os.path.isdir(ac_storage.data_objects["task-labels"].get_path())
        )
        self.assertFalse(os.path.isdir(ac_storage.data_objects["companies"].get_path()))
        self.assertFalse(
            os.path.isdir(ac_storage.data_objects["task-lists"].get_path())
        )
        self.assertFalse(
            os.path.isdir(ac_storage.data_objects["task-history"].get_path())
        )
        self.assertFalse(
            os.path.isdir(ac_storage.data_objects["project-categories"].get_path())
        )
        self.assertFalse(
            os.path.isdir(ac_storage.data_objects["project-notes"].get_path())
        )
        ac_storage.reset()  # reset again should not throw any error
        self.assertEqual(True, True)


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
        self.assertTrue(
            os.path.isdir(ac_storage.data_objects["attachments"].get_path())
        )
        self.assertTrue(
            os.path.isdir(ac_storage.data_objects["project-labels"].get_path())
        )
        self.assertTrue(
            os.path.isdir(ac_storage.data_objects["task-labels"].get_path())
        )
        self.assertTrue(os.path.isdir(ac_storage.data_objects["companies"].get_path()))
        self.assertTrue(os.path.isdir(ac_storage.data_objects["task-lists"].get_path()))
        self.assertTrue(
            os.path.isdir(ac_storage.data_objects["task-history"].get_path())
        )
        self.assertTrue(
            os.path.isdir(ac_storage.data_objects["project-categories"].get_path())
        )
        self.assertTrue(
            os.path.isdir(ac_storage.data_objects["project-notes"].get_path())
        )

    def test_030_get_account_path(self):
        account_id = 12341234
        ac_storage = AcFileStorage(DATA_DIR, account_id)
        self.assertIsNotNone(re.search(str(account_id), ac_storage.get_account_path()))

    # attachments
    @staticmethod
    def _generate_test_attachment(attachment_id: int) -> AcAttachment:
        with open(
            "example-data/example-attachment-29703.json", "r", encoding="utf-8"
        ) as fh:
            attachment = attachment_from_json(json.load(fh))
        attachment.id = attachment_id
        return attachment
