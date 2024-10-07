import json
import os
import shutil

from AcCompany import AcCompany
from AcProjectCategory import AcProjectCategory
from AcProjectLabel import AcProjectLabel
from AcProjectNote import AcProjectNote
from AcTaskHistory import AcTaskHistory
from AcTaskLabel import AcTaskLabel
from AcTaskList import AcTaskList
from ActiveCollabAPI import AC_CLASS_PROJECT, AC_CLASS_COMPANY, AC_CLASS_COMMENT, AC_CLASS_ATTACHMENT_WAREHOUSE, \
    AC_CLASS_PROJECT_NOTE, AC_ERROR_WRONG_CLASS
from ActiveCollabAPI import AC_CLASS_TASK, AC_CLASS_TASK_LABEL, AC_CLASS_TASK_LIST, AC_CLASS_USER_MEMBER
from ActiveCollabAPI import AC_CLASS_USER_OWNER, AC_CLASS_SUBTASK, AC_CLASS_PROJECT_LABEL, AC_CLASS_PROJECT_CATEGORY
from ActiveCollabAPI.AcAttachment import AcAttachment
from ActiveCollabAPI.AcComment import AcComment
from ActiveCollabAPI.AcProject import AcProject
from ActiveCollabAPI.AcSubtask import AcSubtask
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
            os.makedirs(self.get_project_label_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_task_label_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_company_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_task_lists_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_task_history_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_project_category_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_project_notes_path(), DEFAULT_MODE_DIRS)

    def get_account_path(self) -> str:
        return os.path.join(self.root_path, "account-%08d" % self.account_id)

    def get_tasks_path(self) -> str:
        return os.path.join(self.get_account_path(), "tasks")

    @staticmethod
    def get_task_filename(task: AcTask) -> str:
        return "task-%08d.json" % task.id

    # TODO: save_account

    def save_task(self, task: AcTask) -> str:
        assert task.class_ == AC_CLASS_TASK
        task_filename = self.get_task_filename(task)
        task_full_filename = self.get_task_full_filename(task_filename)
        with open(task_full_filename, "w") as f:
            json.dump(task.to_dict(), f, sort_keys=True, indent=2)
        return task_full_filename

    def get_task_full_filename(self, task_filename: str) -> str:
        return os.path.join(self.get_tasks_path(), task_filename)

    def get_projects_path(self) -> str:
        return os.path.join(self.get_account_path(), "projects")

    @staticmethod
    def get_project_filename(project: AcProject) -> str:
        return "project-%08d.json" % project.id

    def get_project_full_filename(self, project_filename: str) -> str:
        return os.path.join(self.get_projects_path(), project_filename)

    def save_project(self, project: AcProject) -> str:
        assert project.class_ == AC_CLASS_PROJECT
        project_filename = self.get_project_filename(project)
        project_full_filename = self.get_project_full_filename(project_filename)
        with open(project_full_filename, "w") as f:
            json.dump(project.to_dict(), f, sort_keys=True, indent=2)
        return project_full_filename

    def get_users_path(self) -> str:
        return os.path.join(self.get_account_path(), "users")

    @staticmethod
    def get_user_filename(user: AcUser) -> str:
        return "user-%08d.json" % user.id

    def get_user_full_filename(self, user_filename: str) -> str:
        return os.path.join(self.get_users_path(), user_filename)

    def save_user(self, user: AcUser) -> str:
        assert user.class_ == AC_CLASS_USER_MEMBER or user.class_ == AC_CLASS_USER_OWNER
        user_filename = self.get_user_filename(user)
        user_full_filename = self.get_user_full_filename(user_filename)
        with open(user_full_filename, "w") as f:
            json.dump(user.to_dict(), f, sort_keys=True, indent=2)
        return user_full_filename

    def get_subtasks_path(self) -> str:
        return os.path.join(self.get_account_path(), "subtasks")

    @staticmethod
    def get_subtask_filename(subtask: AcSubtask) -> str:
        return "subtask-%08d.json" % subtask.id

    def get_subtask_full_filename(self, subtask_filename: str) -> str:
        return os.path.join(self.get_subtasks_path(), subtask_filename)

    def save_subtask(self, subtask: AcSubtask) -> str:
        assert subtask.class_ == AC_CLASS_SUBTASK
        subtask_filename = self.get_subtask_filename(subtask)
        subtask_full_filename = self.get_subtask_full_filename(subtask_filename)
        with open(subtask_full_filename, "w") as f:
            json.dump(subtask.to_dict(), f, sort_keys=True, indent=2)
        return subtask_full_filename

    def get_comments_path(self) -> str:
        return os.path.join(self.get_account_path(), "comments")

    @staticmethod
    def get_comment_filename(comment: AcComment) -> str:
        return "comment-%08d.json" % comment.id

    def get_comment_full_filename(self, comment_filename: str) -> str:
        return os.path.join(self.get_comments_path(), comment_filename)

    def save_comment(self, comment: AcComment) -> str:
        assert comment.class_ == AC_CLASS_COMMENT
        comment_filename = self.get_comment_filename(comment)
        comment_full_filename = self.get_comment_full_filename(comment_filename)
        with open(comment_full_filename, "w") as f:
            json.dump(comment.to_dict(), f, sort_keys=True, indent=2)
        return comment_full_filename

    def get_attachments_path(self) -> str:
        return os.path.join(self.get_account_path(), "attachments")

    @staticmethod
    def get_attachment_filename(attachment: AcAttachment) -> str:
        return "attachment-%08d.json" % attachment.id

    def get_attachment_full_filename(self, attachment_filename: str) -> str:
        return os.path.join(self.get_attachments_path(), attachment_filename)

    def save_attachment(self, attachment: AcAttachment, tmp_download: str) -> str:
        assert attachment.class_ == AC_CLASS_ATTACHMENT_WAREHOUSE
        attachment_filename = self.get_attachment_filename(attachment)
        attachment_full_filename = self.get_attachment_full_filename(attachment_filename)
        with open(attachment_full_filename, "w") as f:
            json.dump(attachment.to_dict(), f, sort_keys=True, indent=2)
        shutil.move(tmp_download, attachment_full_filename + '.' + attachment.extension)
        return attachment_full_filename

    def get_project_label_path(self) -> str:
        return os.path.join(self.get_account_path(), "project-labels")

    @staticmethod
    def get_project_label_filename(project_label: AcProjectLabel) -> str:
        return "project-label-%08d.json" % project_label.id

    def get_project_label_full_filename(self, project_label_filename: str) -> str:
        return os.path.join(self.get_project_label_path(), project_label_filename)

    def save_project_label(self, project_label: AcProjectLabel) -> str:
        assert project_label.class_ == AC_CLASS_PROJECT_LABEL
        project_label_filename = self.get_project_label_filename(project_label)
        project_label_full_filename = self.get_project_label_full_filename(project_label_filename)
        with open(project_label_full_filename, "w") as f:
            json.dump(project_label.to_dict(), f, sort_keys=True, indent=2)
        return project_label_full_filename

    def get_task_label_path(self) -> str:
        return os.path.join(self.get_account_path(), "task-labels")

    @staticmethod
    def get_task_label_filename(task_label: AcTaskLabel) -> str:
        return "task-label-%08d.json" % task_label.id

    def get_task_label_full_filename(self, task_label_filename: str) -> str:
        return os.path.join(self.get_task_label_path(), task_label_filename)

    def save_task_label(self, task_label: AcTaskLabel) -> str:
        assert task_label.class_ == AC_CLASS_TASK_LABEL
        task_label_filename = self.get_task_label_filename(task_label)
        task_label_full_filename = self.get_task_label_full_filename(task_label_filename)
        with open(task_label_full_filename, "w") as f:
            json.dump(task_label.to_dict(), f, sort_keys=True, indent=2)
        return task_label_full_filename

    def get_company_path(self) -> str:
        return os.path.join(self.get_account_path(), "companies")

    @staticmethod
    def get_company_filename(company: AcCompany) -> str:
        return "company-%08d.json" % company.id

    def get_company_full_filename(self, company_filename: str) -> str:
        return os.path.join(self.get_company_path(), company_filename)

    def save_company(self, company: AcCompany) -> str:
        assert company.class_ == AC_CLASS_COMPANY
        company_filename = self.get_company_filename(company)
        company_full_filename = self.get_company_full_filename(company_filename)
        with open(company_full_filename, "w") as f:
            json.dump(company.to_dict(), f, sort_keys=True, indent=2)
        return company_full_filename

    def get_task_lists_path(self) -> str:
        return os.path.join(self.get_account_path(), "task-lists")

    @staticmethod
    def get_task_list_filename(task_list: AcTaskList) -> str:
        return "task-list-%08d.json" % task_list.id

    def get_task_list_full_filename(self, task_list_filename: str) -> str:
        return os.path.join(self.get_task_lists_path(), task_list_filename)

    def save_task_list(self, task_list: AcTaskList) -> str:
        assert task_list.class_ == AC_CLASS_TASK_LIST
        task_list_filename = self.get_task_list_filename(task_list)
        task_list_full_filename = self.get_task_list_full_filename(task_list_filename)
        with open(task_list_full_filename, "w") as f:
            json.dump(task_list.to_dict(), f, sort_keys=True, indent=2)
        return task_list_full_filename

    def get_task_history_path(self) -> str:
        return os.path.join(self.get_account_path(), "task-history")

    @staticmethod
    def get_task_history_filename(task_history: AcTaskHistory) -> str:
        return "task-history-%08d-%010d.json" % (task_history.task_id, task_history.timestamp)

    def get_task_history_full_filename(self, task_history_filename: str) -> str:
        return os.path.join(self.get_task_history_path(), task_history_filename)

    def save_task_history(self, task_history: AcTaskHistory) -> str:
        task_history_filename = self.get_task_history_filename(task_history)
        task_history_full_filename = self.get_task_history_full_filename(task_history_filename)
        with open(task_history_full_filename, "w") as f:
            json.dump(task_history.to_dict(), f, sort_keys=True, indent=2)
        return task_history_full_filename

    def get_project_category_path(self) -> str:
        return os.path.join(self.get_account_path(), "project-category")

    @staticmethod
    def get_project_category_filename(project_category: AcProjectCategory) -> str:
        return "project-category-%04d.json" % project_category.id

    def get_project_category_full_filename(self, project_category_filename: str) -> str:
        return os.path.join(self.get_project_category_path(), project_category_filename)

    def save_project_category(self, project_category: AcProjectCategory) -> str:
        assert project_category.class_ == AC_CLASS_PROJECT_CATEGORY
        project_category_filename = self.get_project_category_filename(project_category)
        project_category_full_filename = self.get_project_category_full_filename(project_category_filename)
        with open(project_category_full_filename, "w") as f:
            json.dump(project_category.to_dict(), f, sort_keys=True, indent=2)
        return project_category_full_filename

    def get_project_notes_path(self) -> str:
        return os.path.join(self.get_account_path(), "project-notes")

    @staticmethod
    def get_project_note_filename(project_note: AcProjectNote) -> str:
        return "project-note-%08d.json" % project_note.id

    def get_project_note_full_filename(self, project_note_filename: str) -> str:
        return os.path.join(self.get_project_notes_path(), project_note_filename)

    def save_project_note(self, project_note: AcProjectNote) -> str:
        assert project_note.class_ == AC_CLASS_PROJECT_NOTE, AC_ERROR_WRONG_CLASS
        project_note_filename = self.get_project_note_filename(project_note)
        project_note_full_filename = self.get_project_note_full_filename(project_note_filename)
        with open(project_note_full_filename, "w") as f:
            json.dump(project_note.to_dict(), f, sort_keys=True, indent=2)
        return project_note_full_filename
