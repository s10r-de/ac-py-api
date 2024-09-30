import json
from unittest import TestCase

from ActiveCollabAPI.AcUser import AcUser, user_from_json


class TestAcUser(TestCase):

    @staticmethod
    def _generate_test_user(user_id: int) -> AcUser:
        with open('../example-data/example-user-00000240.json', 'r') as fh:
            user = user_from_json(json.load(fh))
        user.id = user_id
        return user

    def test_to_dict(self):
        user_id = 100
        user = self._generate_test_user(user_id)
        user_dict = user.to_dict()
        self.assertEqual(user_id, user_dict['id'])

    def test_to_json(self):
        user_id = 102
        user = self._generate_test_user(user_id)
        user_json = user.to_json()
        self.assertEqual(user_id, json.loads(user_json)["id"])
