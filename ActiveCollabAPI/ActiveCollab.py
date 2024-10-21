import random
import string

from AcAttachment import AcAttachment
from AcCompany import AcCompany, company_from_json
from AcFileAccessToken import AcFileAccessToken, fileaccesstoken_from_json
from AcLoginResponse import AcLoginResponse
from AcProjectCategory import AcProjectCategory, project_category_from_json
from AcProjectLabel import AcProjectLabel, project_label_from_json
from AcProjectNote import AcProjectNote, project_note_from_json
from AcTaskHistory import AcTaskHistory, task_history_from_json
from AcTaskLabel import task_label_from_json, AcTaskLabel
from AcTaskList import AcTaskList, task_list_from_json
from ActiveCollabAPI import AC_API_VERSION, AcTask, AC_CLASS_USER_OWNER
from ActiveCollabAPI.AcAccount import AcAccount, account_from_json
from ActiveCollabAPI.AcAuthenticator import AcAuthenticator
from ActiveCollabAPI.AcClient import AcClient
from ActiveCollabAPI.AcCloudLoginResponse import AcCloudLoginResponse
from ActiveCollabAPI.AcComment import AcComment, comment_from_json
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

    This class implements the business logic, it uses the AcClient to call
    the HTTP API to call the Active Collab Server.

    For local persistence we use the AcFileStorage* classes.
    """
    base_url: str = ""

    session: AcSession = None

    def __init__(self, base_url: str, is_cloud: bool = False):
        self.base_url = base_url.rstrip('/')
        self.is_cloud = is_cloud

    def login(self, email: str, password: str, account: str) -> AcSession:
        if self.is_cloud is True:
            self.login_to_cloud(account, email, password)
        else:
            self.login_to_self_hosted(email, password)
        return self.session

    def login_to_self_hosted(self, email, password):
        login_res = self.auth_self_hosted(email, password)
        token = AcToken(login_res.token)
        user = AcLoginUser(avatar_url="",
                           first_name="",
                           last_name="",
                           intent="")
        accounts = []
        cur_account = AcAccount(
            name=0,
            url=self.base_url,
            display_name="self-hosted account",
            user_display_name="self-hosted account",
            position=0,
            class_="",
            status=""
        )
        self.session = AcSession(user, accounts, cur_account, token)

    def login_to_cloud(self, account, email, password):
        login_res = self.auth_cloud(email, password)
        cur_account = self.select_first_account(login_res.accounts)
        if account is not None:
            cur_account = self.select_account(login_res.accounts, account)
        token = self.create_token(cur_account, login_res.user)
        self.session = AcSession(login_res.user, login_res.accounts, cur_account, token)

    def auth_cloud(self, email: str, password: str) -> AcCloudLoginResponse:
        auth = AcAuthenticator(self.base_url)
        res = auth.login_cloud(email, password)
        if res.status_code != 200:
            raise Exception('Login to cloud failed!')
        res_data = res.json()
        if res_data['is_ok'] != 1:
            raise Exception('Login failed! (2)')
        accounts = list(map(lambda a: account_from_json(a), res_data['accounts']))
        user = AcLoginUser(**res_data['user'])
        return AcCloudLoginResponse(user, accounts)

    def auth_self_hosted(self, email: str, password: str) -> AcLoginResponse:
        auth = AcAuthenticator(self.base_url)
        res = auth.login_self_hosted(email, password)
        if res.status_code != 200:
            raise Exception('Login failed!')
        res_data = res.json()
        if res_data['is_ok'] != 1:
            raise Exception('Login failed! (2)')
        return AcLoginResponse(**res_data)

    @staticmethod
    def select_first_account(accounts: list[AcAccount]) -> AcAccount:
        return accounts[0]

    @staticmethod
    def select_account(accounts: list[AcAccount], account: str) -> AcAccount:
        found = list(filter(lambda a: a.display_name == account, accounts))
        if len(found) == 0:
            raise Exception('Account not found!')
        return found[0]

    @staticmethod
    def create_token(account: AcAccount, user: AcLoginUser) -> AcToken:
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

    @staticmethod
    def filter_tasks(tasks: list[AcTask], compare_func: callable) -> list[AcTask]:
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

    def create_user(self, user: AcUser) -> dict | None:
        if user.class_ == AC_CLASS_USER_OWNER:
            print("can not create owner user %d" % user.id)
            return
        client = AcClient(self.session.cur_account, self.session.token)
        user = user.to_dict()
        user["type"] = user["class"]  # FIXME ???
        user["password"] = ''.join(
            random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))  # FIXME ??
        print("QQQ password for user %s is '%s'" % (user["email"], user["password"]))  # FIXME: only for debugging!!
        res = client.post_user(user)
        if res.status_code != 200:
            raise Exception("Error %d - %s" % (res.status_code, str(res.text)))
        res_data = res.json()
        return res_data

    def get_subtasks(self, task: AcTask) -> list[AcSubtask]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_subtasks(task.project_id, task.id)
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        subtasks = list(map(lambda u: subtask_from_json(u), res_data))
        return subtasks

    def get_comments(self, task: AcTask) -> list[AcComment]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_comments(task.id)
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        comments = list(map(lambda c: comment_from_json(c), res_data))
        return comments

    def get_file_access_token(self) -> AcFileAccessToken:
        # Task#35: use TTL to limit amount of requests
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_file_access_token()
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        file_access_token = fileaccesstoken_from_json(res_data)
        return file_access_token

    def download_attachment(self, attachment: AcAttachment) -> str:
        client = AcClient(self.session.cur_account, self.session.token)
        file_access_token = self.get_file_access_token()
        tmp_filename = client.download_attachment(attachment.download_url,
                                                  file_access_token.download_token,
                                                  'attachment_%d_%s' % (attachment.id, attachment.name))
        return tmp_filename

    def get_project_labels(self) -> list[AcProjectLabel]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_project_labels()
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        project_labels = list(map(lambda l: project_label_from_json(l), res_data))
        return project_labels

    def create_project_label(self, project_label: AcProjectLabel) -> dict | None:
        client = AcClient(self.session.cur_account, self.session.token)
        project_label = project_label.to_dict()
        project_label["type"] = project_label["class"]  # FIXME
        res = client.post_project_label(project_label)
        if res.status_code != 200:
            raise Exception("Error %d - %s" % (res.status_code, str(res.text)))
        res_data = res.json()
        return res_data

    def get_task_labels(self) -> list[AcTaskLabel]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_task_labels()
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        task_labels = list(map(lambda u: task_label_from_json(u), res_data))
        return task_labels

    def get_all_companies(self) -> list[AcCompany]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_all_companies()
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        companies = list(map(lambda u: company_from_json(u), res_data))
        return companies

    def create_company(self, company: AcCompany) -> dict | None:
        if company.is_owner is True:
            print("skip owner company %d" % company.id)
            return
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.post_company(company.to_dict())
        if res.status_code != 200:
            raise Exception("Error %d - %s" % (res.status_code, str(res.text)))
        res_data = res.json()
        return res_data

    def get_project_task_lists(self, project: AcProject) -> list[AcTaskList]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_task_lists(project.id)
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        task_lists = list(map(lambda t: task_list_from_json(t), res_data))
        return task_lists

    def get_task_history(self, task: AcTask) -> list[AcTaskHistory]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_task_history(task.id)
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        task_history = list(map(lambda u: task_history_from_json(u, task_id=task.id), res_data))
        return task_history

    def get_project_categories(self) -> list[AcProjectCategory]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_project_categories()
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        project_categories = list(map(lambda l: project_category_from_json(l), res_data))
        return project_categories

    def create_project_category(self, project_category: AcProjectCategory) -> dict | None:
        client = AcClient(self.session.cur_account, self.session.token)
        project_category = project_category.to_dict()
        project_category["type"] = project_category["class"]  # FIXME
        res = client.post_project_category(project_category)
        if res.status_code != 200:
            raise Exception("Error %d - %s" % (res.status_code, str(res.text)))
        res_data = res.json()
        return res_data

    def get_project_notes(self, project: AcProject) -> list[AcProjectNote]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_project_notes(project.id)
        if res.status_code != 200:
            raise Exception("Error %d" % res.status_code)
        res_data = res.json()
        project_notes = list(map(lambda l: project_note_from_json(l), res_data))
        return project_notes
