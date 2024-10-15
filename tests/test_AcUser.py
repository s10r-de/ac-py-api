import json
from unittest import TestCase

from ActiveCollabAPI import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_
from ActiveCollabAPI.AcUser import user_from_json


class TestAcUser(TestCase):

    @staticmethod
    def _generate_test_user(user_id: int) -> dict:
        with open('example-data/example-user-00000240.json', 'r') as fh:
            user_json = json.load(fh)
        user_json["id"] = user_id
        return user_json

    def test_to_dict(self):
        user_id = 100
        user_json = self._generate_test_user(user_id)
        user = user_from_json(user_json)
        user_dict = user.to_dict()
        self.assertEqual(user_id, user_dict['id'])
        self.assertIn(AC_PROPERTY_CLASS, user_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, user_dict.keys())

    def test_to_json(self):
        user_id = 102
        user_json = self._generate_test_user(user_id)
        user = user_from_json(user_json)
        user_json = user.to_json()
        self.assertEqual(user_id, json.loads(user_json)["id"])
        self.assertIn(AC_PROPERTY_CLASS, json.loads(user_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(user_json).keys())
