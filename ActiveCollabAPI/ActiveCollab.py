from ActiveCollabAPI import AC_API_VERSION
from ActiveCollabAPI.AcAuthenticator import AcAuthenticator
from ActiveCollabAPI.AcClient import AcClient
from ActiveCollabAPI.AcTokenAuthenticator import AcTokenAuthenticator
from ActiveCollabAPI.AcAccount import AcAccount, account_from_json
from ActiveCollabAPI.AcLoginResponse import AcLoginResponse
from ActiveCollabAPI.AcSession import AcSession
from ActiveCollabAPI.AcToken import AcToken
from ActiveCollabAPI.AcUser import AcUser


class ActiveCollab:
    """
    Active Collab Client library coming from the use case
    """
    base_url: str = ""

    session: AcSession = None

    def __init__(self, base_url: str):
        self.base_url = base_url

    def login_to_account(self, email: str, password: str, account: str | None) -> AcSession:
        login_res = self.user_login(email, password)
        cur_account = self.select_first_account(login_res.accounts)
        if account is not None:
            cur_account = self.select_account(login_res.accounts, account)
        token = self.create_token(cur_account, login_res.user)
        self.session = AcSession(login_res.user, login_res.accounts, cur_account, token)
        return self.session

    def user_login(self, email: str, password: str) -> AcLoginResponse:
        auth = AcAuthenticator(self.base_url)
        res = auth.login(email, password)
        if res.status_code != 200:
            raise Exception('Login failed!')
        res_data = res.json()
        if res_data['is_ok'] != 1:
            raise Exception('Login failed! (2)')
        accounts = list(map(lambda a: account_from_json(a), res_data['accounts']))
        return AcLoginResponse(AcUser(**res_data['user']), accounts)

    def select_first_account(self, accounts: list[AcAccount]) -> AcAccount:
        return accounts[0]

    def select_account(self, accounts: list[AcAccount], account: str) -> AcAccount:
        found = list(filter(lambda a: a.display_name == account, accounts))
        if len(found) == 0:
            raise Exception('Account not found!')
        return found[0]

    def create_token(self, account: AcAccount, user: AcUser) -> AcToken:
        authenticator = AcTokenAuthenticator(account.url + '/api/v%s' % AC_API_VERSION)
        res = authenticator.issue_token_intent(user.intent)
        if res.status_code != 200:
            raise Exception('Request token failed!')
        res_data = res.json()
        if res_data['is_ok'] != 1:
            raise Exception('Request token failed! (2)')
        return AcToken(res_data["token"])

    def get_info(self):
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_info()
        return res.json()
