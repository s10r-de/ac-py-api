import inspect
import os.path
import time
from unittest import TestCase

from AcStorage.AcFileStorageProjectLabel import AcFileStorageProjectLabel
from active_collab_api.AcProjectLabel import project_label_from_json
from active_collab_api import AC_ERROR_WRONG_CLASS

DATA_DIR = "./data-test/%s/" % __name__
ACCOUNT_ID = 12345


class TestAcFileStorageProjectLabel(TestCase):
    @staticmethod
    def _generate_test_project_label(label_id: int) -> dict:
        return {
            "id": label_id,
            "class": "ProjectLabel",
            "url_path": "/projects/label/%d" % label_id,
            "name": "Test Project Label",
            "updated_on": int(time.time()),
            "color": "#ff00ff",
            "lighter_text_color": "#ffa0ff",
            "darker_text_color": "#a0a0a0",
            "is_default": True,
            "position": 1,
            "project_id": 56,
        }

    def test_save(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageProjectLabel(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        project_label = project_label_from_json(self._generate_test_project_label(3))
        full_filename = storage.save(project_label)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))

    def test_save_wrong_class(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageProjectLabel(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        project_label = project_label_from_json(self._generate_test_project_label(30))
        project_label.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(project_label)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
