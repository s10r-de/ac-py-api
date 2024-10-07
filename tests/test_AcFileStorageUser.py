import json
import os.path
from unittest import TestCase

from AcFileStorageUser import AcFileStorageUser
from AcUser import user_from_json
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS

DATA_DIR = './data'
ACCOUNT_ID = 12345


class TestAcFileStorageUser(TestCase):

    @staticmethod
    def _generate_test_user(user_id: int) -> dict:
        with open('../example-data/example-user-00000240.json', 'r') as fh:
            user_json = json.load(fh)
        user_json["id"] = user_id
        return user_json

    def test_get_path(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageUser(DATA_DIR, account_id)
        self.assertGreater(len(storage.get_path()), 1)

    def test_reset(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageUser(DATA_DIR, account_id)
        storage.reset()
        self.assertFalse(os.path.isdir(storage.get_path()))

    def test_ensure_dirs(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageUser(DATA_DIR, account_id)
        storage.ensure_dirs()
        self.assertTrue(os.path.isdir(storage.get_path()))

    def test_get_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageUser(DATA_DIR, account_id)
        user = user_from_json(self._generate_test_user(35))
        filename = storage.get_filename(user)
        self.assertGreater(len(filename), 0)

    def test_get_full_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageUser(DATA_DIR, account_id)
        user = user_from_json(self._generate_test_user(34))
        filename = storage.get_filename(user)
        full_filename = storage.get_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_save(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageUser(DATA_DIR, account_id)
        storage.reset()
        storage.ensure_dirs()
        user = user_from_json(self._generate_test_user(36))
        full_filename = storage.save(user)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))
        # test catch the wrong class
        user2 = user_from_json(self._generate_test_user(360))
        user2.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(user2)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
