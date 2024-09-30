import json
from unittest import TestCase

from AcAttachment import attachment_from_json, AcAttachment
from AcComment import AcComment, comment_from_json


class TestAcComment(TestCase):

    @staticmethod
    def _generate_test_comment(comment_id: int) -> AcComment:
        with open('../example-data/example-comment-95993.json', 'r') as fh:
            comment = comment_from_json(json.load(fh))
        comment.id = comment_id
        return comment

    @staticmethod
    def _generate_test_attachment(attachment_id: int) -> AcAttachment:
        with open('../example-data/example-attachment-29703.json', 'r') as fh:
            attachment = attachment_from_json(json.load(fh))
        attachment.id = attachment_id
        return attachment

    def test_attachment_constructor(self):
        comment_id = 59234
        comment = self._generate_test_comment(comment_id)
        self.assertEqual(comment_id, comment.id)

    def test_to_dict(self):
        comment_id = 59234
        comment = self._generate_test_comment(comment_id)
        comment_dict = comment.to_dict()
        self.assertEqual(comment_id, comment_dict["id"])

    def test_to_json(self):
        comment_id = 59234
        comment = self._generate_test_comment(comment_id)
        comment_json = comment.to_json()
        self.assertEqual(comment_id, json.loads(comment_json)["id"])

    def test_get_attachments(self):
        comment_id = 17614
        comment = self._generate_test_comment(comment_id)
        comment.attachments = [
            self._generate_test_attachment(78),
            self._generate_test_attachment(79)
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
            self._generate_test_attachment(79)
        ]
        comment_dict = comment.to_dict()
        self.assertEqual(comment_id, comment_dict["id"])
        self.assertEqual(2, len(comment_dict["attachments"]))
        self.assertEqual("WarehouseAttachment", comment_dict["attachments"][0]["class"])
        self.assertEqual("WarehouseAttachment", comment_dict["attachments"][1]["class"])

    def test_to_json_with_attachments(self):
        comment_id = 17614
        comment = self._generate_test_comment(comment_id)
        comment.attachments = [
            self._generate_test_attachment(78),
            self._generate_test_attachment(79)
        ]
        comment_json = comment.to_json()
        parsed_json = json.loads(comment_json)
        self.assertEqual(comment_id, parsed_json["id"])
        self.assertEqual(2, len(parsed_json["attachments"]))
        self.assertEqual("WarehouseAttachment", parsed_json["attachments"][0]["class"])
        self.assertEqual("WarehouseAttachment", parsed_json["attachments"][1]["class"])

    @staticmethod
    def _generate_test_comment_with_attachments(comment_id: int) -> AcComment:
        with open('../example-data/example-comment-95993b.json', 'r') as fh:
            comment = comment_from_json(json.load(fh))
        comment.id = comment_id
        return comment

    def test_from_json_with_attachments(self):
        comment_id = 17614
        comment = self._generate_test_comment_with_attachments(comment_id)
        attachments = comment.get_attachments()
        self.assertEqual(2, len(attachments))
        self.assertIsInstance(attachments[0], AcAttachment)
        self.assertIsInstance(attachments[1], AcAttachment)
