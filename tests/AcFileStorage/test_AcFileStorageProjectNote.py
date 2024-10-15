import inspect
import json
import os.path
from unittest import TestCase, skipIf

from AcFileStorageProjectNote import AcFileStorageProjectNote
from AcProjectNote import project_note_from_json
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS

DATA_DIR = './data-test/%s/' % __name__
ACCOUNT_ID = 12345


class TestAcFileStorageProjectNote(TestCase):

    @staticmethod
    def _generate_test_project_note(note_id: int) -> dict:
        with open("example-data/example-note-94-without-attachment.json", "r") as f:
            project_note_json = json.load(f)
        project_note_json["id"] = note_id
        return project_note_json

    @staticmethod
    def _generate_test_project_note_with_2_attachements(note_id: int) -> dict:
        with open("example-data/example-note-87-with-2-attachments.json", "r") as f:
            project_note_json = json.load(f)
        project_note_json["id"] = note_id
        return project_note_json

    def test_save(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageProjectNote(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        project_note = project_note_from_json(self._generate_test_project_note(3))
        full_filename = storage.save(project_note)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))

    def test_save_with_wrong_class(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageProjectNote(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        project_note = project_note_from_json(self._generate_test_project_note(30))
        project_note.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(project_note)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])

    def test_save_with_attachments(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageProjectNote(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        project = project_note_from_json(self._generate_test_project_note_with_2_attachements(4))
        full_filename = storage.save(project)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))

    def test_save_with_attachments_wrong_class(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageProjectNote(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        project_note = project_note_from_json(self._generate_test_project_note_with_2_attachements(40))
        project_note.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(project_note)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])

    @skipIf(True, "attachements not yet impelemented")
    def test_save_with_attachments_wrong_class_in_attachment(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageProjectNote(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        project_note = project_note_from_json(self._generate_test_project_note_with_2_attachements(40))
        project_note.attachments[0].class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(project_note)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
