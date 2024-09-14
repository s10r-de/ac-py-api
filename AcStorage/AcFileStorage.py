import json
import os
import shutil

from AcAttachment import AcAttachment
from ActiveCollabAPI import AcSubtask
from ActiveCollabAPI.AcComment import AcComment
from ActiveCollabAPI.AcProject import AcProject
from ActiveCollabAPI.AcTask import AcTask
from ActiveCollabAPI.AcUser import AcUser

DEFAULT_MODE_DIRS = 0o700


class AcFileStorage(object):

    def __init__(self, root_path: str, account_id: int):
        self.root_path = root_path
        self.account_id = account_id

    def reset(self):
        if os.path.exists(self.root_path):
            shutil.rmtree(self.root_path)

    def ensure_dirs(self):
        if not os.path.exists(self.get_account_path()):
            os.makedirs(self.get_account_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_tasks_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_projects_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_users_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_subtasks_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_comments_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_attachments_path(), DEFAULT_MODE_DIRS)

    def get_account_path(self) -> str:
        return os.path.join(self.root_path, "account-%08d" % self.account_id)

    def get_tasks_path(self) -> str:
        return os.path.join(self.get_account_path(), "tasks")

    def get_task_filename(self, task: AcTask) -> str:
        return "task-%08d.json" % task.id

    def save_task(self, task: AcTask) -> str:
        task_filename = self.get_task_filename(task)
        task_full_filename = self.get_task_full_filename(task_filename)
        with open(task_full_filename, "w") as f:
            json.dump(task.to_dict(), f, sort_keys=True, indent=2)
        return task_full_filename

    def get_task_full_filename(self, task_filename: str) -> str:
        return os.path.join(self.get_tasks_path(), task_filename)

    def get_projects_path(self) -> str:
        return os.path.join(self.get_account_path(), "projects")

    def get_project_filename(self, project: AcProject) -> str:
        return "project-%08d.json" % project.id

    def get_project_full_filename(self, project_filename: str) -> str:
        return os.path.join(self.get_projects_path(), project_filename)

    def save_project(self, project: AcProject) -> str:
        project_filename = self.get_project_filename(project)
        project_full_filename = self.get_project_full_filename(project_filename)
        with open(project_full_filename, "w") as f:
            json.dump(project.to_dict(), f, sort_keys=True, indent=2)
        return project_full_filename

    def get_users_path(self) -> str:
        return os.path.join(self.get_account_path(), "users")

    def get_user_filename(self, user: AcUser) -> str:
        return "user-%08d.json" % user.id

    def get_user_full_filename(self, user_filename: str) -> str:
        return os.path.join(self.get_users_path(), user_filename)

    def save_user(self, user: AcUser) -> str:
        user_filename = self.get_user_filename(user)
        user_full_filename = self.get_user_full_filename(user_filename)
        with open(user_full_filename, "w") as f:
            json.dump(user.to_dict(), f, sort_keys=True, indent=2)
        return user_full_filename

    def get_subtasks_path(self) -> str:
        return os.path.join(self.get_account_path(), "subtasks")

    def get_subtask_filename(self, subtask: AcSubtask) -> str:
        return "subtask-%08d.json" % subtask.id

    def get_subtask_full_filename(self, subtask_filename: str) -> str:
        return os.path.join(self.get_subtasks_path(), subtask_filename)

    def save_subtask(self, subtask: AcSubtask) -> str:
        subtask_filename = self.get_subtask_filename(subtask)
        subtask_full_filename = self.get_subtask_full_filename(subtask_filename)
        with open(subtask_full_filename, "w") as f:
            json.dump(subtask.to_dict(), f, sort_keys=True, indent=2)
        return subtask_full_filename

    def get_comments_path(self) -> str:
        return os.path.join(self.get_account_path(), "comments")

    def get_comment_filename(self, comment: AcComment) -> str:
        return "comment-%08d.json" % comment.id

    def get_comment_full_filename(self, comment_filename: str) -> str:
        return os.path.join(self.get_comments_path(), comment_filename)

    def save_comment(self, comment: AcComment) -> str:
        comment_filename = self.get_comment_filename(comment)
        comment_full_filename = self.get_comment_full_filename(comment_filename)
        with open(comment_full_filename, "w") as f:
            json.dump(comment.to_dict(), f, sort_keys=True, indent=2)
        return comment_full_filename

    def get_attachments_path(self) -> str:
        return os.path.join(self.get_account_path(), "attachments")

    def get_attachment_filename(self, attachment: AcAttachment) -> str:
        return "attachment-%08d.json" % attachment.id

    def get_attachment_full_filename(self, attachment_filename: str) -> str:
        return os.path.join(self.get_attachments_path(), attachment_filename)

    def save_attachment(self, attachment: AcAttachment, tmp_download: str) -> str:
        attachment_filename = self.get_attachment_filename(attachment)
        attachment_full_filename = self.get_attachment_full_filename(attachment_filename)
        with open(attachment_full_filename, "w") as f:
            json.dump(attachment.to_dict(), f, sort_keys=True, indent=2)
        shutil.copyfile(tmp_download, attachment_full_filename + '.' + attachment.extension)
        return attachment_full_filename
