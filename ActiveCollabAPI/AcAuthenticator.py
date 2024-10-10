# system libs
import json

# 3rd party libs
import requests
from requests import Response

from ActiveCollabAPI import AC_USER_AGENT, AC_API_CLIENT_VENDOR, AC_API_CLIENT_NAME, AC_API_VERSION


class AcAuthenticator:
    base_url: str = ""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/') + '/api/v%d' % AC_API_VERSION

    @staticmethod
    def headers():
        return {
            'Content-Type': 'application/json; charset=utf8',
            'Accept': 'application/json',
            'User-Agent': AC_USER_AGENT
        }

    def login_cloud(self, email: str, password: str) -> Response:
        login_data = {
            'email': email,
            'password': password
        }
        return requests.post(self.base_url + "/external/login",
                             data=json.dumps(login_data),
                             headers=self.headers())

    def login_self_hosted(self, email: str, password: str) -> Response:
        login_data = {
            'username': email,
            'password': password,
            'client_name': AC_API_CLIENT_NAME,
            'client_vendor': AC_API_CLIENT_VENDOR
        }
        return requests.post(self.base_url + "/issue-token",
                             data=json.dumps(login_data),
                             headers=self.headers())
