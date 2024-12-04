import hashlib
import json
import logging
import os
import time
from tempfile import gettempdir

import requests
from requests import Response

from active_collab_api import AC_API_VERSION, AC_USER_AGENT
from active_collab_api.ac_account import AcAccount
from active_collab_api.ac_token import AcToken

DEFAULT_TIMEOUT = 15


class AcClient:
    """
    Active Collab REST API Client

    This class implements only the basic HTTP API handling and not
    the business logic.  For the business logic look into class "ActiveCollab".

    """

    base_url = ""
    account: AcAccount
    token: AcToken

    def __init__(self, account: AcAccount, token: AcToken):
        self.account = account
        self.token = token
        #
        self.base_url = self.account.url + "/api/v%d" % AC_API_VERSION

    def headers(self):
        return {
            "Content-Type": "application/json; charset=utf8",
            "Accept": "application/json",
            "X-Angie-AuthApiToken": self.token.token,
            "User-Agent": AC_USER_AGENT,
        }

    def _get(self, url: str, retry=3, pause=5) -> Response:
        res = requests.get(
            self.base_url + "/" + url, headers=self.headers(), timeout=DEFAULT_TIMEOUT
        )
        if res.status_code >= 500:
            if retry > 0:
                logging.warning("Got status code %d in GET %s" % (res.status_code, url))
                logging.warning("+ Retry No.%d in %d seconds..." % (retry, pause))
                time.sleep(pause)
                res = self._get(url, retry=retry - 1)
        return res

    def _delete(self, url: str) -> Response:
        return requests.delete(
            self.base_url + "/" + url, headers=self.headers(), timeout=DEFAULT_TIMEOUT
        )

    def _post(self, url: str, data: str, files=None) -> Response:
        return requests.post(
            self.base_url + "/" + url,
            headers=self.headers(),
            data=data,
            files=files,
            timeout=DEFAULT_TIMEOUT,
        )

    def _upload(self, url: str, files: dict) -> Response:
        headers = self.headers()
        del headers["Content-Type"]
        return requests.post(
            self.base_url + "/" + url,
            headers=headers,
            files=files,
            timeout=DEFAULT_TIMEOUT,
        )

    def _put(self, url: str, data: str) -> Response:
        return requests.put(
            self.base_url + "/" + url,
            headers=self.headers(),
            data=data,
            timeout=DEFAULT_TIMEOUT,
        )

    def get_info(self):
        return self._get("info")

    def get_trash(self) -> Response:
        return self._get("trash")

    def delete_trash(self) -> Response:
        return self._delete("trash")

    # tasks

    def get_project_active_tasks(self, project_id: int):
        return self._get("projects/%d/tasks" % project_id)

    def post_task(self, data: dict) -> Response:
        project_id = data["project_id"]
        data["labels"] = list(map(lambda task: task["name"], data["labels"]))
        return self._post("projects/%d/tasks" % project_id, json.dumps(data))

    def complete_task(self, task_id: int) -> Response:
        return self._put("complete/task/%d" % task_id, "")

    def delete_task(self, project_id: int, task_id: int) -> Response:
        return self._delete("projects/%d/tasks/%d" % (project_id, task_id))

    def get_project_completed_tasks(self, project_id: int):
        return self._get("projects/%d/tasks/archive" % project_id)

    def update_task_assign_file(
        self,
        project_id: int,
        task_id: int,
        disposition: str,
        code: str,
    ) -> Response:
        data = {
            "disposition": disposition,
            "attach_uploaded_files": [
                code,
            ],
        }
        return self._put(
            "projects/%d/tasks/%d" % (project_id, task_id), json.dumps(data)
        )

    # projects

    def get_active_projects(self):
        return self._get("projects")

    def get_archived_projects(self):
        return self._get("projects/archive")

    def post_project(self, data: dict) -> Response:
        return self._post("projects", json.dumps(data))

    def complete_project(self, project_id: int) -> Response:
        return self._put("complete/project/%d" % project_id, "")

    def delete_project(self, project_id: int) -> Response:
        return self._delete("projects/%d" % project_id)

    # notes

    def get_project_notes(self, project_id: int):
        return self._get("projects/%d/notes" % project_id)

    def update_note_assign_file(
        self,
        project_id: int,
        parent_type: str,
        parent_id: int,
        disposition: str,
        code: str,
    ) -> Response:
        data = {
            "notes_id": parent_id,
            "disposition": disposition,
            "attach_uploaded_files": [
                code,
            ],
        }
        return self._put(
            "projects/%d/notes/%d" % (project_id, parent_id), json.dumps(data)
        )

    # users

    def get_all_users(self):
        return self._get("users/all")

    def delete_user(self, user_id: int) -> Response:
        return self._delete("users/%d" % user_id)

    def post_user(self, data: dict) -> Response:
        return self._post("users", json.dumps(data))

    def archive_user(self, user_id: int) -> Response:
        return self._put("/move-to-archive/user/%d" % user_id, "")

    # subtasks

    def get_subtasks(self, project_id: int, task_id: int):
        return self._get("projects/%d/tasks/%d/subtasks" % (project_id, task_id))

    def post_subtask(self, project_id: int, task_id: int, data: dict) -> Response:
        return self._post(
            "projects/%d/tasks/%d/subtasks" % (project_id, task_id), json.dumps(data)
        )

    def complete_subtask(self, subtask_id: int) -> Response:
        return self._put("complete/subtask/%d" % subtask_id, "")

    # comments

    def get_comments(self, task_id: int):
        return self._get("comments/task/%d" % task_id)

    def post_comment(self, parent_type: str, parent_id: int, data: dict) -> Response:
        return self._post("comments/%s/%d" % (parent_type, parent_id), json.dumps(data))

    def update_comment_assign_file(
        self,
        comment_id: int,
        disposition: str,
        name: str,
        code: str,
    ) -> Response:
        data = {
            "name": name,
            "disposition": disposition,
            "attach_uploaded_files": [
                code,
            ],
        }
        return self._put("comments/%d" % comment_id, json.dumps(data))

    # attachments

    def get_attachment(self, attachment_id: int):
        return self._get("attachments/%d" % attachment_id)

    def get_file_access_token(self, retry=3, pause=5) -> Response:
        res = requests.get(
            self.base_url + "/issue-file-access-token", headers=self.headers()
        )
        if res.status_code >= 500:
            if retry > 0:
                logging.warning("GET file_access_token got status %d" % res.status_code)
                logging.warning("Retry No.%d in %d seconds..." % (retry, pause))
                time.sleep(pause)
                res = self.get_file_access_token(retry=retry - 1)
        return res

    def download_attachment(
        self, download_url: str, file_access_token: str, filename: str
    ) -> str:
        # replace &intent=--DOWNLOAD-TOKEN--  with download token
        download_url = download_url.replace(
            "intent=--DOWNLOAD-TOKEN--", "intent=%s" % file_access_token
        )
        download_url = download_url.replace(
            "i=--DOWNLOAD-TOKEN--", "i=%s" % file_access_token
        )
        with requests.get(download_url, headers=self.headers(), stream=True) as r:
            r.raise_for_status()
            tmp_filename = os.path.join(gettempdir(), filename)
            tmp_filename_safe = hashlib.sha256(tmp_filename.encode("utf-8")).hexdigest()
            with open(tmp_filename_safe, "w+b") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return tmp_filename_safe

    def upload_files(self, files: dict) -> Response:
        return self._upload("upload-files", files=files)

    # project labels

    def get_project_labels(self) -> Response:
        return self._get("labels/project-labels")

    def post_project_label(self, data: dict) -> Response:
        return self._post("labels", json.dumps(data))

    def delete_project_label(self, project_label_id: int) -> Response:
        return self._delete("labels/%d" % project_label_id)

    # task labels

    def get_task_labels(self) -> Response:
        return self._get("labels/task-labels")

    # companies

    def get_all_companies(self) -> Response:
        return self._get("companies/all")

    def delete_company(self, company_id: int) -> Response:
        return self._delete("companies/%d" % company_id)

    def post_company(self, data: dict) -> Response:
        return self._post("companies", json.dumps(data))

    # task list

    def get_task_lists(self, project_id: int) -> Response:
        return self._get("projects/%d/task-lists" % project_id)

    def get_archived_task_lists(self, project_id: int) -> Response:
        return self._get("projects/%d/task-lists/archive" % project_id)

    def post_task_list(self, data: dict) -> Response:
        project_id = data["project_id"]
        return self._post("projects/%d/task-lists" % project_id, json.dumps(data))

    def complete_task_list(self, task_list_id: int) -> Response:
        return self._put("complete/task-list/%d" % task_list_id, "")

    def delete_task_list(self, project_id: int, task_list_id: int) -> Response:
        return self._delete("projects/%d/task-lists/%d" % (project_id, task_list_id))

    # task history

    def get_task_history(self, task_id: int):
        return self._get("history/task/%d?verbose=1" % task_id)

    # category

    def get_project_categories(self) -> Response:
        return self._get("projects/categories")

    def delete_project_category(self, project_category_id: int) -> Response:
        return self._delete("categories/%d" % project_category_id)

    def post_project_category(self, data: dict) -> Response:
        return self._post("categories", json.dumps(data))
