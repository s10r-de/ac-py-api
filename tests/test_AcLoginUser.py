import json
from unittest import TestCase

from AcLoginUser import AcLoginUser


class TestAcLoginUser(TestCase):

    def test_to_dict(self):
        first_name = "Carsten"
        intent = "alskdjflkadsjfkldsajfk"
        login_user = AcLoginUser(
            avatar_url="https://avatar.example.com",
            first_name=first_name,
            last_name="Last name",
            intent=intent
        )
        login_user_dict = login_user.to_dict()
        self.assertEqual(first_name, login_user_dict['first_name'])

    def test_to_json(self):
        first_name = "Carsten"
        intent = "alskdjflkadsjfkldsajfk"
        login_user = AcLoginUser(
            avatar_url="https://avatar.example.com",
            first_name=first_name,
            last_name="Last name",
            intent=intent
        )
        login_user_json = login_user.to_json()
        self.assertEqual(first_name, json.loads(login_user_json)["first_name"])
