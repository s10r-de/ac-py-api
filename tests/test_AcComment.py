import json
from unittest import TestCase

from ActiveCollabAPI.AcAttachment import attachment_from_json, AcAttachment
from ActiveCollabAPI.AcComment import AcComment, comment_from_json
from ActiveCollabAPI import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_, AC_ERROR_WRONG_CLASS


class TestAcComment(TestCase):
    @staticmethod
    def _generate_test_comment(comment_id: int) -> AcComment:
        with open("tests/example-data/example-comment-95993.json", "r") as fh:
            comment = comment_from_json(json.load(fh))
        comment.id = comment_id
        return comment

    @staticmethod
    def _generate_test_attachment(attachment_id: int) -> AcAttachment:
        with open("tests/example-data/example-attachment-29703.json", "r") as fh:
            attachment = attachment_from_json(json.load(fh))
        attachment.id = attachment_id
        return attachment

    def test_attachment_constructor(self):
        comment_id = 59233
        comment = self._generate_test_comment(comment_id)
        self.assertEqual(comment_id, comment.id)

    def test_to_dict(self):
        comment_id = 59234
        comment = self._generate_test_comment(comment_id)
        comment_dict = comment.to_dict()
        self.assertEqual(comment_id, comment_dict["id"])
        self.assertIn(AC_PROPERTY_CLASS, comment_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, comment_dict.keys())

    def test_to_json(self):
        comment_id = 59234
        comment = self._generate_test_comment(comment_id)
        comment_json = comment.to_json()
        self.assertEqual(comment_id, json.loads(comment_json)["id"])
        self.assertIn(AC_PROPERTY_CLASS, json.loads(comment_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(comment_json).keys())

    def test_from_json_wrong_class(self):
        comment_id = 17614
        comment = self._generate_test_comment_with_attachments(comment_id)
        comment["class"] = "dummy"
        with self.assertRaises(AssertionError) as cm:
            comment_from_json(comment)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])

    def test_get_attachments(self):
        comment_id = 17614
        comment = self._generate_test_comment(comment_id)
        comment.attachments = [
            self._generate_test_attachment(78),
            self._generate_test_attachment(79),
        ]
        attachments = comment.get_attachments()
        self.assertEqual(2, len(attachments))
        self.assertIsInstance(attachments[0], AcAttachment)
        self.assertIsInstance(attachments[1], AcAttachment)

    def test_to_dict_with_attachments(self):
        comment_id = 17614
        comment = self._generate_test_comment(comment_id)
        comment.attachments = [
            self._generate_test_attachment(78),
            self._generate_test_attachment(79),
        ]
        comment_dict = comment.to_dict()
        self.assertEqual(comment_id, comment_dict["id"])
        self.assertEqual(2, len(comment_dict["attachments"]))
        self.assertEqual("WarehouseAttachment",
                         comment_dict["attachments"][0]["class"])
        self.assertEqual("WarehouseAttachment",
                         comment_dict["attachments"][1]["class"])

    def test_to_json_with_attachments(self):
        comment_id = 17614
        comment = self._generate_test_comment(comment_id)
        comment.attachments = [
            self._generate_test_attachment(78),
            self._generate_test_attachment(79),
        ]
        comment_json = comment.to_json()
        parsed_json = json.loads(comment_json)
        self.assertEqual(comment_id, parsed_json["id"])
        self.assertEqual(2, len(parsed_json["attachments"]))
        self.assertEqual("WarehouseAttachment",
                         parsed_json["attachments"][0]["class"])
        self.assertEqual("WarehouseAttachment",
                         parsed_json["attachments"][1]["class"])

    @staticmethod
    def _generate_test_comment_with_attachments(comment_id: int) -> dict:
        with open("tests/example-data/example-comment-95993b.json", "r") as fh:
            comment = json.load(fh)
        comment["id"] = comment_id
        return comment

    def test_from_json_with_attachments(self):
        comment_id = 17614
        comment_json = self._generate_test_comment_with_attachments(comment_id)
        comment = comment_from_json(comment_json)
        attachments = comment.get_attachments()
        self.assertEqual(2, len(attachments))
        self.assertIsInstance(attachments[0], AcAttachment)
        self.assertIsInstance(attachments[1], AcAttachment)
