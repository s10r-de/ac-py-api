import json
from unittest import TestCase

from AcAccount import AcAccount, account_from_json


class TestAcAccount(TestCase):

    @staticmethod
    def _generate_test_account(account_id: int) -> AcAccount:
        return AcAccount(
            name=account_id,
            url="'https://app.activecollab.com/%d" % account_id,
            display_name="#%d" % account_id,
            user_display_name="Account display name",
            position=1,
            class_='ActiveCollab\\Shepherd\\Model\\Account\\ActiveCollab\\FeatherAccount',
            status="active"
        )

    def test_to_dict(self):
        account_id = 100
        user = self._generate_test_account(account_id)
        user_dict = user.to_dict()
        self.assertEqual(user_dict['name'], account_id)

    def test_to_json(self):
        account_id = 102
        account = self._generate_test_account(account_id)
        account_json = account.to_json()
        self.assertEqual(json.loads(account_json)["name"], account_id)

    def test_account_from_json(self):
        account_id = 103
        account_json = {
            "name": account_id,
            "url": "'https://app.activecollab.com/%d" % account_id,
            "display_name": "#%d" % account_id,
            "user_display_name": "Account display name",
            "position": 1,
            "class": 'ActiveCollab\\Shepherd\\Model\\Account\\ActiveCollab\\FeatherAccount',
            "status": "active"
        }
        account = account_from_json(account_json)
        self.assertEqual(account.name, account_json["name"])
