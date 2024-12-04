from unittest import TestCase

from active_collab_api.AcFileAccessToken import fileaccesstoken_from_json


class TestAcFileAccessToken(TestCase):
    def test_account_from_json(self):
        token_json = {
            "download_token": "bla",
            "preview_token": "bla 2",
            "thumb_token": "bla 3",
            "ttl": 3600,
        }
        token = fileaccesstoken_from_json(token_json)
        self.assertEqual(token.ttl, token_json["ttl"])
