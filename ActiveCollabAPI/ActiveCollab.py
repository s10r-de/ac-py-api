from ActiveCollabAPI import AC_API_VERSION, AcTask
from ActiveCollabAPI.AcAccount import AcAccount, account_from_json
from ActiveCollabAPI.AcAuthenticator import AcAuthenticator
from ActiveCollabAPI.AcClient import AcClient
from ActiveCollabAPI.AcLoginResponse import AcLoginResponse
from ActiveCollabAPI.AcLoginUser import AcLoginUser
from ActiveCollabAPI.AcProject import AcProject, project_from_json
from ActiveCollabAPI.AcSession import AcSession
from ActiveCollabAPI.AcSubtask import AcSubtask, subtask_from_json
from ActiveCollabAPI.AcTask import task_from_json
from ActiveCollabAPI.AcToken import AcToken
from ActiveCollabAPI.AcTokenAuthenticator import AcTokenAuthenticator
from ActiveCollabAPI.AcUser import AcUser, user_from_json


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
        return AcLoginResponse(AcLoginUser(**res_data['user']), accounts)

    def select_first_account(self, accounts: list[AcAccount]) -> AcAccount:
        return accounts[0]

    def select_account(self, accounts: list[AcAccount], account: str) -> AcAccount:
        found = list(filter(lambda a: a.display_name == account, accounts))
        if len(found) == 0:
            raise Exception('Account not found!')
        return found[0]

    def create_token(self, account: AcAccount, user: AcLoginUser) -> AcToken:
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

    def get_active_tasks(self, project_id: int) -> list[AcTask]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_project_active_tasks(project_id)
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        tasks = list(map(lambda p: task_from_json(p), res_data['tasks']))
        return tasks

    def get_completed_tasks(self, project_id: int) -> list[AcTask]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_project_completed_tasks(project_id)
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        tasks = list(map(lambda p: task_from_json(p), res_data))
        return tasks

    def filter_tasks(self, tasks: list[AcTask], compare_func: callable) -> list[AcTask]:
        return list(filter(compare_func, tasks))

    def get_active_projects(self) -> list[AcProject]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_active_projects()
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        projects = list(map(lambda p: project_from_json(p), res_data))
        return projects

    def get_archived_projects(self) -> list[AcProject]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_archived_projects()
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        projects = list(map(lambda p: project_from_json(p), res_data))
        return projects

    def get_all_users(self) -> list[AcUser]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_all_users()
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        users = list(map(lambda u: user_from_json(u), res_data))
        return users

    def get_subtasks(self, task: AcTask) -> list[AcSubtask]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_subtasks(task.project_id, task.id)
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        subtasks = list(map(lambda u: subtask_from_json(u), res_data))
        return subtasks
