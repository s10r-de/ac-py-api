import json

import requests
from requests import Response

from ActiveCollabAPI import AC_USER_AGENT, AC_API_CLIENT_NAME, AC_API_CLIENT_VENDOR


class AcTokenAuthenticator:
    base_url = ""

    def __init__(self, base_url: str):
        self.base_url = base_url

    @staticmethod
    def headers():
        return {
            'Content-Type': 'application/json; charset=utf8',
            'Accept': 'application/json',
            'User-Agent': AC_USER_AGENT
        }

    def issue_token_intent(self, intent: str) -> Response:
        # use intent to get a token
        data = {
            'intent': intent,
            'client_name': AC_API_CLIENT_NAME,
            'client_vendor': AC_API_CLIENT_VENDOR
        }
        return requests.post(self.base_url + '/issue-token-intent',
                             headers=self.headers(),
                             data=json.dumps(data))
