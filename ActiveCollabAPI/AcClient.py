import json

import requests

from ActiveCollabAPI import AC_USER_AGENT, AC_API_VERSION
from ActiveCollabAPI.AcAccount import AcAccount
from ActiveCollabAPI.AcToken import AcToken


class AcClient:
    """
    Active Collab REST API Client
    """
    base_url = None
    account = None
    token = None

    def __init__(self, account: AcAccount, token: AcToken):
        self.account = account
        self.token = token
        #
        self.base_url = self.account.url + '/api/v%d' % AC_API_VERSION

    def headers(self):
        return {
            'Content-Type': 'application/json; charset=utf8',
            'Accept': 'application/json',
            'X-Angie-AuthApiToken': self.token.token,
            'User-Agent': AC_USER_AGENT
        }

    def _get(self, url):
        return requests.get(self.base_url + '/' + url,
                            headers=self.headers())

    def _delete(self, url):
        return requests.delete(self.base_url + '/' + url,
                               headers=self.headers())

    def _post(self, url, data):
        return requests.post(
            self.base_url + '/' + url,
            headers=self.headers(),
            data=json.dumps(data))

    def _put(self, url, data):
        return requests.put(
            self.base_url + '/' + url,
            headers=self.headers(),
            data=json.dumps(data))

    def get_info(self):
        return self._get('info')

    def get_project_tasks(self, project_id: int):
        return self._get('projects/%d/tasks' % project_id)
