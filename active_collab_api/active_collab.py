import logging

from active_collab_api import (
    AC_API_VERSION,
    AC_CLASS_COMMENT,
    AC_CLASS_PROJECT_NOTE,
    AC_CLASS_TASK,
    AC_CLASS_USER_OWNER,
)
from active_collab_api.ac_account import AcAccount, account_from_json
from active_collab_api.ac_api_error import AcApiError
from active_collab_api.ac_attachment import AcAttachment
from active_collab_api.ac_attachment_upload_response import (
    attachment_upload_response_from_json,
)
from active_collab_api.ac_authenticator import AcAuthenticator
from active_collab_api.ac_client import AcClient
from active_collab_api.ac_cloud_login_response import AcCloudLoginResponse
from active_collab_api.ac_comment import AcComment, comment_from_json
from active_collab_api.ac_company import AcCompany, company_from_json
from active_collab_api.ac_file_access_token import (
    AcFileAccessToken,
    fileaccesstoken_from_json,
)
from active_collab_api.ac_login_response import AcLoginResponse
from active_collab_api.ac_login_user import AcLoginUser
from active_collab_api.ac_project import AcProject, project_from_json
from active_collab_api.ac_project_category import (
    AcProjectCategory,
    project_category_from_json,
)
from active_collab_api.ac_project_label import AcProjectLabel, project_label_from_json
from active_collab_api.ac_project_note import AcProjectNote, project_note_from_json
from active_collab_api.ac_session import AcSession
from active_collab_api.ac_subtask import (
    AcSubtask,
    subtask_from_json,
    subtask_map_name_to_text,
)
from active_collab_api.ac_task import AcTask, task_from_json
from active_collab_api.ac_task_history import AcTaskHistory, task_history_from_json
from active_collab_api.ac_task_label import AcTaskLabel, task_label_from_json
from active_collab_api.ac_task_list import AcTaskList, task_list_from_json
from active_collab_api.ac_token import AcToken
from active_collab_api.ac_token_authenticator import AcTokenAuthenticator
from active_collab_api.ac_user import (
    AcUser,
    generate_random_password,
    map_cloud_user_language_id,
    user_from_json,
)


def _workaround_user_fix_type_from_class(user: AcUser) -> AcUser:
    user.type = user.class_
    return user


def _workaround_project_fix_type_from_class(project: AcProject) -> AcProject:
    project.type = project.class_
    return project


class ActiveCollab:
    """
    Active Collab Client library coming from the use case

    This class implements the business logic, it uses the AcClient to call
    the HTTP API to call the Active Collab Server.

    For local persistence we use the AcFileStorage* classes.
    """

    base_url: str = ""

    session: AcSession

    def __init__(self, base_url: str, is_cloud: bool = False):
        self.base_url = base_url.rstrip("/")
        self.is_cloud = is_cloud

    def login(self, email: str, password: str, account: str) -> AcSession:
        if self.is_cloud is True:
            self.login_to_cloud(account, email, password)
        else:
            self.login_to_self_hosted(email, password)
        return self.session

    def login_to_cloud(self, account, email, password):
        login_res = self.auth_cloud(email, password)
        cur_account = self.select_first_account(login_res.accounts)
        if account is not None:
            cur_account = self.select_account(login_res.accounts, account)
        token = self.create_token(cur_account, login_res.user)
        self.session = AcSession(login_res.user, login_res.accounts, cur_account, token)
        self.client = AcClient(self.session.cur_account, self.session.token)

    def auth_cloud(self, email: str, password: str) -> AcCloudLoginResponse:
        auth = AcAuthenticator(self.base_url)
        res = auth.login_cloud(email, password)
        if res.status_code != 200:
            raise AcApiError("Login to cloud failed!")
        res_data = res.json()
        if res_data["is_ok"] != 1:
            raise AcApiError("Login failed! (2)")
        accounts = list(map(account_from_json, res_data["accounts"]))
        user = AcLoginUser(**res_data["user"])
        return AcCloudLoginResponse(user, accounts)

    def login_to_self_hosted(self, email, password):
        login_res = self.auth_self_hosted(email, password)
        token = AcToken(login_res.token)
        user = AcLoginUser(avatar_url="", first_name="", last_name="", intent="")
        accounts = []
        cur_account = AcAccount(
            name=0,
            url=self.base_url,
            display_name="self-hosted account",
            user_display_name="self-hosted account",
            position=0,
            class_="",
            status="",
        )
        self.session = AcSession(user, accounts, cur_account, token)
        self.client = AcClient(self.session.cur_account, self.session.token)

    def auth_self_hosted(self, email: str, password: str) -> AcLoginResponse:
        auth = AcAuthenticator(self.base_url)
        res = auth.login_self_hosted(email, password)
        if res.status_code != 200:
            raise AcApiError("Login failed!")
        res_data = res.json()
        if res_data["is_ok"] != 1:
            raise AcApiError("Login failed! (2)")
        return AcLoginResponse(**res_data)

    @staticmethod
    def select_first_account(accounts: list[AcAccount]) -> AcAccount:
        return accounts[0]

    @staticmethod
    def select_account(accounts: list[AcAccount], account: str) -> AcAccount:
        found = list(filter(lambda a: a.display_name == account, accounts))
        if len(found) == 0:
            raise AcApiError("Account not found!")
        return found[0]

    @staticmethod
    def create_token(account: AcAccount, user: AcLoginUser) -> AcToken:
        authenticator = AcTokenAuthenticator(account.url + "/api/v%s" % AC_API_VERSION)
        res = authenticator.issue_token_intent(user.intent)
        if res.status_code != 200:
            raise AcApiError("Request token failed!")
        res_data = res.json()
        if res_data["is_ok"] != 1:
            raise AcApiError("Request token failed! (2)")
        return AcToken(res_data["token"])

    def get_info(self):
        res = self.client.get_info()
        return res.json()

    def get_all_tasks(self, project_id: int) -> list[AcTask]:
        tasks = self.get_active_tasks(project_id)
        tasks.extend(self.get_completed_tasks(project_id))
        return tasks

    def get_active_tasks(self, project_id: int) -> list[AcTask]:
        res = self.client.get_project_active_tasks(project_id)
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        tasks = list(map(task_from_json, res_data["tasks"]))
        return tasks

    def get_completed_tasks(self, project_id: int) -> list[AcTask]:
        res = self.client.get_project_completed_tasks(project_id)
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        tasks = list(map(task_from_json, res_data))
        return tasks

    def complete_task(self, task: AcTask) -> dict | None:
        logging.debug("Complete task: " + task.to_json())
        res = self.client.complete_task(task.id)
        if res.status_code != 200:
            logging.error("Error %d - %s" % (res.status_code, str(res.text)))
            return None
        res_data = res.json()
        return res_data

    def create_task(self, task: AcTask) -> dict | None:
        logging.debug("Create task: " + task.to_json())
        task.type = task.class_  # FIXME
        res = self.client.post_task(task.to_dict())
        if res.status_code == 404:
            logging.error(task.to_dict())
            logging.error(
                "Project %d not found! Can not create task!" % task.project_id
            )
            return None
        if res.status_code != 200:
            logging.error(task.to_dict())
            logging.error("Error %d - %s" % (res.status_code, str(res.text)))
            return None
        res_data = res.json()
        return res_data

    def update_task_set_task_number(self, task: AcTask) -> dict | None:
        logging.debug("Set the task number %s", task.to_json())
        task_dict = {
            "task_number": task.task_number
        }
        res = self.client.put_task(task.project_id, task.id, task_dict)
        if res.status_code == 404:
            logging.error(task.to_dict())
            logging.error(
                "Project %d or Task %d not found! Can not update task!" % (task.project_id, task.id)
            )
            return None
        if res.status_code != 200:
            logging.error(task.to_dict())
            logging.error("Error %d - %s" % (res.status_code, str(res.text)))
            return None
        res_data = res.json()
        return res_data

    def delete_all_tasks(self, project_id: int) -> list[AcTask]:
        tasks = []
        for task in self.get_all_tasks(project_id):
            tasks.append(task)
            self.client.delete_task(project_id, task.id)
        return tasks

    def delete_all_task_lists(self, project: AcProject) -> list[AcTask]:
        result = []
        for task in self.get_project_task_lists(project.id):
            result.extend(self.client.delete_task_list(project.id, task.id))
        return result

    @staticmethod
    def filter_tasks(tasks: list[AcTask], compare_func: callable) -> list[AcTask]:
        return list(filter(compare_func, tasks))

    def get_all_projects(self) -> list[AcProject]:
        projects = self.get_active_projects()
        projects.extend(self.get_archived_projects())
        return projects

    def get_active_projects(self) -> list[AcProject]:
        res = self.client.get_active_projects()
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        projects = list(map(project_from_json, res_data))
        return projects

    def get_archived_projects(self) -> list[AcProject]:
        res = self.client.get_archived_projects()
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        projects = list(map(project_from_json, res_data))
        return projects

    def complete_project(self, project: AcProject) -> dict | None:
        res = self.client.complete_project(project.id)
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        return res_data

    def create_project(self, project: AcProject) -> dict | None:
        logging.debug("Creating project %s", project.to_json())
        project = _workaround_project_fix_type_from_class(project)
        res = self.client.post_project(project.to_dict())
        if res.status_code != 200:
            logging.error(project.to_dict())
            logging.error(
                "cant create project! (%d - %s)" % (res.status_code, res.text)
            )
            return None
        res_data = res.json()
        return res_data

    def update_project_set_project_number(self, project: AcProject) -> dict | None:
        logging.debug("Set the project_number %s", project.to_json())
        project = _workaround_project_fix_type_from_class(project)
        project_dict = {
            "project_number": project.project_number
        }
        res = self.client.put_project(project.id, project_dict)
        if res.status_code == 404:
            logging.error(project.to_dict())
            logging.error(
                "Project %d not found! Can not update project!" % project.id
            )
            return None
        if res.status_code != 200:
            logging.error(project.to_dict())
            logging.error(
                "cant update project! (%d - %s)" % (res.status_code, res.text)
            )
            return None
        res_data = res.json()
        return res_data

    def delete_all_projects(self) -> None:
        for project in self.get_all_projects():
            self.client.delete_project(project.id)

    def delete_all_project_categories(self) -> None:
        for project_category in self.get_project_categories():
            self.client.delete_project_category(project_category.id)

    def delete_all_project_labels(self) -> None:
        for project_label in self.get_project_labels():
            self.client.delete_project_label(project_label.id)

    def get_all_users(self) -> list[AcUser]:
        res = self.client.get_all_users()
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        users = list(map(user_from_json, res_data))
        return users

    def create_user(self, user: AcUser) -> bool:
        logging.debug("create user: " + user.to_json())
        if user.class_ == AC_CLASS_USER_OWNER:
            logging.warning("can not create owner user %d" % user.id)
            return False
        user = _workaround_user_fix_type_from_class(user)
        user = map_cloud_user_language_id(user)
        user = generate_random_password(user)
        res = self.client.post_user(user.to_dict())
        if res.status_code != 200:
            logging.error(user.to_dict())
            logging.error("Error %d - %s" % (res.status_code, str(res.text)))
            return False
        return True

    def archive_user(self, user: AcUser) -> dict | None:
        res = self.client.archive_user(user.id)
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        return res_data

    def get_subtasks(self, task: AcTask) -> list[AcSubtask]:
        res = self.client.get_subtasks(task.project_id, task.id)
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        subtasks = list(map(subtask_from_json, res_data))
        return subtasks

    def complete_subtask(self, subtask: AcSubtask) -> dict | None:
        logging.debug("Complete subtask: " + subtask.to_json())
        res = self.client.complete_subtask(subtask.id)
        if res.status_code != 200:
            logging.error("Error %d - %s" % (res.status_code, str(res.text)))
            return None
        res_data = res.json()
        return res_data

    def create_subtask(self, subtask: AcSubtask) -> dict | None:
        logging.debug("Create subtask: " + subtask.to_json())
        subtask.type = subtask.class_  # FIXME
        subtask = subtask_map_name_to_text(subtask)
        res = self.client.post_subtask(
            subtask.project_id, subtask.task_id, subtask.to_dict()
        )
        if res.status_code == 404:
            logging.error(
                "Project %d or Task %d not found! Can not create subtask! (%d, %s)"
                % (subtask.project_id, subtask.task_id, res.status_code, res.text)
            )
            return None
        if res.status_code != 200:
            logging.error("Error %d - %s" % (res.status_code, str(res.text)))
            return None
        res_data = res.json()
        return res_data

    def get_comments(self, task: AcTask) -> list[AcComment]:
        res = self.client.get_comments(task.id)
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        comments = list(map(comment_from_json, res_data))
        return comments

    def create_comment(self, comment: AcComment) -> dict | None:
        logging.debug("Create comment: " + comment.to_json())
        comment.type = comment.class_  # FIXME
        comment.parent_type = comment.parent_type.lower()
        res = self.client.post_comment(
            comment.parent_type, comment.parent_id, comment.to_dict()
        )
        if res.status_code == 404:
            logging.error(
                "Parent %s/%d not found! Can not create comment!"
                % (comment.parent_type, comment.parent_id)
            )
            return None
        if res.status_code != 200:
            logging.error("Error %d - %s" % (res.status_code, str(res.text)))
            return None
        res_data = res.json()
        return res_data

    def get_file_access_token(self) -> AcFileAccessToken:
        # Task#35: use TTL to limit amount of requests
        res = self.client.get_file_access_token()
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        file_access_token = fileaccesstoken_from_json(res_data)
        return file_access_token

    def download_attachment(self, attachment: AcAttachment) -> str:
        file_access_token = self.get_file_access_token()
        tmp_filename = self.client.download_attachment(
            attachment.download_url,
            file_access_token.download_token,
            "attachment_%d_%s" % (attachment.id, attachment.name),
        )
        return tmp_filename

    def upload_attachment(self, attachment: AcAttachment, bin_file: str) -> dict:
        """
        Upload a saved file to the Server.

        Note: The API would support upload of multiple files but our
        current implemenation handles only one file!
        """
        with open(bin_file, "rb") as fh:
            # 1. upload file
            files = {
                "file": (
                    attachment.name,
                    fh,
                    attachment.mime_type,
                )
            }
            res = self.client.upload_files(files)
            if res.status_code != 200:
                msg = "Error %d - %s" % (res.status_code, str(res.text))
                logging.error(msg)
                raise AcApiError(msg)
            logging.debug("Upload file response: %s" % res.text)
            res_data = res.json()
            attachment_upload_response = attachment_upload_response_from_json(
                res_data[0]
            )

            # assign file to the parent
            if attachment.parent_type == AC_CLASS_TASK:
                res = self.client.update_task_assign_file(
                    project_id=attachment.project_id,
                    task_id=attachment.parent_id,
                    disposition=attachment.disposition,
                    code=attachment_upload_response.code,
                )
            if attachment.parent_type == AC_CLASS_COMMENT:
                res = self.client.update_comment_assign_file(
                    comment_id=attachment.parent_id,
                    disposition=attachment.disposition,
                    name=attachment.name,
                    code=attachment_upload_response.code,
                )
            if attachment.parent_type == AC_CLASS_PROJECT_NOTE:
                logging.info("Attachments for notes not yet implemented!")
                return {}

            if res.status_code == 404:
                logging.error(
                    "Parent %s/%d not found! Can not create attachment!"
                    % (attachment.parent_type, attachment.parent_id)
                )
                return {}
            if res.status_code != 200:
                msg = "Error %d - %s" % (res.status_code, str(res.text))
                raise AcApiError(msg)
            res_data = res.json()
            return res_data

    def get_project_labels(self) -> list[AcProjectLabel]:
        res = self.client.get_project_labels()
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        project_labels = list(map(project_label_from_json, res_data))
        return project_labels

    def create_project_label(self, project_label: AcProjectLabel) -> dict | None:
        logging.debug("create project label: " + project_label.to_json())
        project_label.type = project_label.class_  # FIXME
        res = self.client.post_project_label(project_label.to_dict())
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code} {res.text}")
        res_data = res.json()
        return res_data

    def get_task_labels(self) -> list[AcTaskLabel]:
        res = self.client.get_task_labels()
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        task_labels = list(map(task_label_from_json, res_data))
        return task_labels

    def get_all_companies(self) -> list[AcCompany]:
        res = self.client.get_all_companies()
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        companies = list(map(company_from_json, res_data))
        return companies

    def create_company(self, company: AcCompany) -> AcCompany:
        logging.debug("create company: " + company.to_json())
        if company.is_owner is True:
            logging.warning("skip owner company %d" % company.id)
            return False
        res = self.client.post_company(company.to_dict())
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code} {res.text}")
        return company_from_json(res.json())

    def empty_trash(self) -> dict:
        client = AcClient(self.session.cur_account, self.session.token)
        # FIXME loop until empty
        trash = client.get_trash()
        client.delete_trash()
        return trash.json()

    def delete_all_users(self) -> None:
        for user in self.get_all_users():
            if user.class_ != AC_CLASS_USER_OWNER:
                self.client.delete_user(user.id)

    def delete_all_companies(self) -> None:
        for company in self.get_all_companies():
            if company.is_owner is False:
                self.client.delete_company(company.id)

    def get_project_task_lists(self, project_id: int) -> list[AcTaskList]:
        res = self.client.get_task_lists(project_id)
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        task_lists = list(map(task_list_from_json, res_data))
        return task_lists

    def get_project_archived_task_lists(self, project_id: int) -> list[AcTaskList]:
        client = AcClient(self.session.cur_account, self.session.token)
        res = client.get_archived_task_lists(project_id)
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        task_lists = list(map(task_list_from_json, res_data))
        return task_lists

    def get_project_all_task_lists(self, project: AcProject) -> list[AcTaskList]:
        task_lists = self.get_project_task_lists(project.id)
        task_lists.extend(self.get_project_archived_task_lists(project.id))
        return task_lists

    def complete_task_list(self, task_list: AcTaskList) -> dict | None:
        logging.debug("create task list: " + task_list.to_json())
        res = self.client.complete_task_list(task_list.id)
        if res.status_code != 200:
            logging.error("Error %d - %s" % (res.status_code, str(res.text)))
            return None
        res_data = res.json()
        return res_data

    def create_task_list(self, task_list: AcTaskList) -> dict | None:
        logging.debug("create task list: " + task_list.to_json())
        task_list.type = task_list.class_  # FIXME
        res = self.client.post_task_list(task_list.to_dict())
        if res.status_code == 404:
            logging.error(task_list.to_dict())
            logging.error(
                "Project %d not found! Can not create task list!" % task_list.project_id
            )
            return None
        if res.status_code != 200:
            logging.error(task_list.to_dict())
            logging.error("Error %d - %s" % (res.status_code, str(res.text)))
            return None
        res_data = res.json()
        return res_data

    def get_task_history(self, task: AcTask) -> list[AcTaskHistory]:
        res = self.client.get_task_history(task.id)
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        task_history = list(
            map(lambda u: task_history_from_json(u, task_id=task.id), res_data)
        )
        return task_history

    def get_project_categories(self) -> list[AcProjectCategory]:
        res = self.client.get_project_categories()
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        project_categories = list(map(project_category_from_json, res_data))
        return project_categories

    def create_project_category(
        self, project_category: AcProjectCategory
    ) -> dict | None:
        logging.debug("create project category: " + project_category.to_json())
        project_category.type = project_category.class_  # FIXME
        res = self.client.post_project_category(project_category.to_dict())
        if res.status_code != 200:
            logging.error(project_category.to_dict())
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        return res_data

    def get_project_notes(self, project: AcProject) -> list[AcProjectNote]:
        res = self.client.get_project_notes(project.id)
        if res.status_code != 200:
            raise AcApiError(f"Error {res.status_code}")
        res_data = res.json()
        project_notes = list(map(project_note_from_json, res_data))
        return project_notes
