from unittest import TestCase

from active_collab_api.AcAccount import AcAccount
from active_collab_api.AcCloudLoginResponse import AcCloudLoginResponse
from active_collab_api.AcLoginUser import AcLoginUser


class TestAcLoginResponse(TestCase):
    def test_ac_login_response_constructor(self):
        first_name = "Carsten"
        intent = "alskdjflkadsjfkldsajfk"
        account_id = 4711

        login_user = AcLoginUser(
            avatar_url="https://avatar.example.com",
            first_name=first_name,
            last_name="Last name",
            intent=intent,
        )

        account = AcAccount(
            name=account_id,
            url="'https://app.activecollab.com/%d" % account_id,
            display_name="#%d" % account_id,
            user_display_name="Account display name",
            position=1,
            class_="ActiveCollab\\Shepherd\\Model\\Account\\ActiveCollab\\FeatherAccount",
            status="active",
        )

        response = AcCloudLoginResponse(user=login_user, accounts=[account])
        self.assertIsInstance(response, AcCloudLoginResponse)
        self.assertEqual(first_name, response.user.first_name)
        self.assertEqual(account_id, response.accounts[0].name)
