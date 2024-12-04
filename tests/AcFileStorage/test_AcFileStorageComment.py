import inspect
import json
import os.path
from unittest import TestCase

from active_collab_api.AcComment import comment_from_json
from active_collab_storage.AcFileStorageComment import AcFileStorageComment
from active_collab_api import AC_ERROR_WRONG_CLASS

DATA_DIR = "./data-test/%s/" % __name__
ACCOUNT_ID = 12345


class TestAcFileStorageComment(TestCase):
    @staticmethod
    def _generate_test_comment(comment_id: int) -> dict:
        with open("tests/example-data/example-comment-95993.json", "r") as fh:
            comment = json.load(fh)
        comment["id"] = comment_id
        return comment

    def test_save(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageComment(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        comment = comment_from_json(self._generate_test_comment(57))
        filename = storage.save(comment)
        self.assertTrue(os.path.isfile(filename))

    def test_save_wrong_class(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageComment(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        comment = comment_from_json(self._generate_test_comment(58))
        comment.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(comment)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
