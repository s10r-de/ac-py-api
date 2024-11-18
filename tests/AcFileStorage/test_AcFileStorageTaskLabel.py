import inspect
import os.path
import time
from unittest import TestCase

from AcFileStorageTaskLabel import AcFileStorageTaskLabel
from AcTaskLabel import task_label_from_json
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS

DATA_DIR = './data-test/%s/' % __name__
ACCOUNT_ID = 12345


class TestAcFileStorageTaskLabel(TestCase):

    @staticmethod
    def _generate_test_task_label(label_id: int) -> dict:
        return {
            "id": label_id,
            "class_": "TaskLabel",
            "url_path": "/task/label/%d" % label_id,
            "name": "Test Task Label",
            "updated_on": int(time.time()),
            "color": "#ff00ff",
            "lighter_text_color": "#ffa0ff",
            "darker_text_color": "#a0a0a0",
            "is_default": True,
            "is_global": True,
            "position": 3,
            "project_id": 34
        }

    def test_save(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageTaskLabel(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        task_label = task_label_from_json(self._generate_test_task_label(36))
        full_filename = storage.save(task_label)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))

    def test_save_wrong_class(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageTaskLabel(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        task_label = task_label_from_json(self._generate_test_task_label(360))
        task_label.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(task_label)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
