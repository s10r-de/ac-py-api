import inspect
import json
import os.path
from unittest import TestCase

from active_collab_storage.AcFileStorageUser import AcFileStorageUser
from active_collab_api.AcUser import user_from_json
from active_collab_api import AC_ERROR_WRONG_CLASS

DATA_DIR = "./data-test/%s/" % __name__
ACCOUNT_ID = 12345


class TestAcFileStorageUser(TestCase):
    @staticmethod
    def _generate_test_user(user_id: int) -> dict:
        with open("tests/example-data/example-user-00000240.json", "r") as fh:
            user_json = json.load(fh)
        user_json["id"] = user_id
        return user_json

    def test_save(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageUser(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        user = user_from_json(self._generate_test_user(36))
        full_filename = storage.save(user)
        self.assertTrue(os.path.isfile(full_filename))

    def test_save_wrong_class(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageUser(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        user = user_from_json(self._generate_test_user(37))
        storage.save(user)
        user.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(user)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
