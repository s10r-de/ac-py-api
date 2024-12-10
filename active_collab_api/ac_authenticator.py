# system libs
import json

# 3rd party libs
import requests
from requests import Response

from active_collab_api import (
    AC_API_CLIENT_NAME,
    AC_API_CLIENT_VENDOR,
    AC_API_VERSION,
    AC_USER_AGENT,
)
from active_collab_api.ac_client import DEFAULT_TIMEOUT


class AcAuthenticator:
    base_url: str = ""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/") + f"/api/v{AC_API_VERSION}"
        self.session = requests.Session()

    @staticmethod
    def headers():
        return {
            "Content-Type": "application/json; charset=utf8",
            "Accept": "application/json",
            "User-Agent": AC_USER_AGENT,
        }

    def login_cloud(self, email: str, password: str) -> Response:
        login_data = {"email": email, "password": password}
        return self.session.post(
            self.base_url + "/external/login",
            data=json.dumps(login_data),
            headers=self.headers(),
            timeout=DEFAULT_TIMEOUT,
        )

    def login_self_hosted(self, email: str, password: str) -> Response:
        login_data = {
            "username": email,
            "password": password,
            "client_name": AC_API_CLIENT_NAME,
            "client_vendor": AC_API_CLIENT_VENDOR,
        }
        return self.session.post(
            self.base_url + "/issue-token",
            data=json.dumps(login_data),
            headers=self.headers(),
            timeout=DEFAULT_TIMEOUT,
        )
