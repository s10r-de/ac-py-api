import json
from unittest import TestCase

from AcAttachment import attachment_from_json
from ActiveCollabAPI import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


class TestAcAttachment(TestCase):

    @staticmethod
    def _generate_test_attachment(attachment_id: int) -> dict:
        with open('example-data/example-attachment-29703.json', 'r') as fh:
            attachment_json = json.load(fh)
        attachment_json["id"] = attachment_id
        return attachment_json

    def test_to_dict(self):
        attachment_id = 7
        attachment_json = self._generate_test_attachment(attachment_id)
        attachment = attachment_from_json(attachment_json)
        attachment_dict = attachment.to_dict()
        self.assertEqual(attachment_id, attachment_dict['id'])
        self.assertIn(AC_PROPERTY_CLASS, attachment_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, attachment_dict.keys())

    def test_to_json(self):
        attachment_id = 8
        attachment_json = self._generate_test_attachment(attachment_id)
        attachment = attachment_from_json(attachment_json)
        attachment_json = attachment.to_json()
        self.assertEqual(attachment_id, json.loads(attachment_json)["id"])
        self.assertIn(AC_PROPERTY_CLASS, json.loads(attachment_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(attachment_json).keys())
