import json
from unittest import TestCase

from AcAttachment import AcAttachment
from AcProjectNote import project_note_from_json
from ActiveCollabAPI import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_, AC_CLASS_PROJECT_NOTE, AC_ERROR_WRONG_CLASS


class TestAcProjectNote(TestCase):

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

    def test_from_json(self):
        note_id = 735
        project_note_json = self._generate_test_project_note(note_id)
        project_note = project_note_from_json(project_note_json)
        self.assertEqual(note_id, project_note.id)
        #
        project_note_json = self._generate_test_project_note(note_id + 2)
        project_note_json[AC_PROPERTY_CLASS] = "dummy"
        with self.assertRaises(AssertionError) as cm:
            project_note = project_note_from_json(project_note_json)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
        self.assertEqual(note_id, project_note.id)

    def test_from_json_with_attachments(self):
        note_id = 735
        project_note_json = self._generate_test_project_note_with_2_attachements(note_id)
        project_note = project_note_from_json(project_note_json)
        self.assertEqual(note_id, project_note.id)
        self.assertEqual(2, len(project_note.attachments))
        self.assertIsInstance(project_note.attachments[0], AcAttachment)
        #
        project_note_json = self._generate_test_project_note_with_2_attachements(note_id + 2)
        project_note_json[AC_PROPERTY_CLASS] = "dummy"
        with self.assertRaises(AssertionError) as cm:
            project_note = project_note_from_json(project_note_json)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
        self.assertEqual(note_id, project_note.id)

    def test_to_dict(self):
        note_id = 736
        project_note_json = self._generate_test_project_note(note_id)
        project_note = project_note_from_json(project_note_json)
        project_note = project_note.to_dict()
        self.assertEqual(note_id, project_note["id"])
        self.assertEqual(AC_CLASS_PROJECT_NOTE, project_note["class"], )
        self.assertIn(AC_PROPERTY_CLASS, project_note.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, project_note.keys())

    def test_to_dict_with_2_attachments(self):
        note_id = 736
        project_note_json = self._generate_test_project_note_with_2_attachements(note_id)
        project_note = project_note_from_json(project_note_json)
        project_note = project_note.to_dict()
        self.assertEqual(note_id, project_note["id"])
        self.assertEqual(AC_CLASS_PROJECT_NOTE, project_note["class"], )
        self.assertIn(AC_PROPERTY_CLASS, project_note.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, project_note.keys())
        self.assertEqual(2, len(project_note["attachments"]))

    def test_to_json(self):
        note_id = 737
        project_note_json = self._generate_test_project_note(note_id)
        project_note = project_note_from_json(project_note_json)
        project_note_json = project_note.to_json()
        self.assertEqual(note_id, json.loads(project_note_json)["id"])
        self.assertEqual(AC_CLASS_PROJECT_NOTE, json.loads(project_note_json)["class"], )
        self.assertIn(AC_PROPERTY_CLASS, json.loads(project_note_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(project_note_json).keys())
