import json
import logging

import requests

from ActiveCollabAPI import AC_USER_AGENT, AC_API_VERSION
from ActiveCollabAPI.AcAccount import AcAccount
from ActiveCollabAPI.AcToken import AcToken

DEBUG = True

if DEBUG:
    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    import http.client as http_client

    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


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

    def get_project_active_tasks(self, project_id: int):
        return self._get('projects/%d/tasks' % project_id)

    def get_project_completed_tasks(self, project_id: int):
        return self._get('projects/%d/tasks/archive' % project_id)

    def get_active_projects(self):
        return self._get('projects')

    def get_archived_projects(self):
        return self._get('projects/archive')

    def get_all_users(self):
        return self._get('users/all')
