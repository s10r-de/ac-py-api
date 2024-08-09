# system libs
import json

# 3rd party libs
import requests
from requests import Response

from ActiveCollabAPI import AC_USER_AGENT


class AcAuthenticator:
    base_url: str = ""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def headers(self):
        return {
            'Content-Type': 'application/json; charset=utf8',
            'Accept': 'application/json',
            'User-Agent': AC_USER_AGENT
        }

    def login(self, email: str, password: str) -> Response:
        login_data = {
            'email': email,
            'password': password
        }
        return requests.post(self.base_url,
                             data=json.dumps(login_data),
                             headers=self.headers())
