import json
import os
import shutil
import time

from AcFileStorageCompany import AcFileStorageCompany
from AcFileStorageProject import AcFileStorageProject
from AcFileStorageProjectCategory import AcFileStorageProjectCategory
from AcFileStorageProjectLabel import AcFileStorageProjectLabel
from AcFileStorageProjectNote import AcFileStorageProjectNote
from AcFileStorageTask import AcFileStorageTask
from AcFileStorageTaskLabel import AcFileStorageTaskLabel
from AcFileStorageTaskList import AcFileStorageTaskList
from AcFileStorageUser import AcFileStorageUser
from AcStorage import DEFAULT_MODE_DIRS
from AcTaskHistory import AcTaskHistory
from ActiveCollabAPI import AC_CLASS_COMMENT, AC_CLASS_ATTACHMENT_WAREHOUSE
from ActiveCollabAPI import AC_CLASS_SUBTASK
from ActiveCollabAPI.AcAttachment import AcAttachment
from ActiveCollabAPI.AcComment import AcComment
from ActiveCollabAPI.AcSubtask import AcSubtask


class AcFileStorage:

    def __init__(self, root_path: str, account_id: int):
        self.root_path = root_path
        self.account_id = account_id
        self.data_objects = {}
        self.data_objects["company"] = AcFileStorageCompany(root_path, account_id)
        self.data_objects["users"] = AcFileStorageUser(root_path, account_id)
        self.data_objects["projects"] = AcFileStorageProject(root_path, account_id)
        self.data_objects["project-categories"] = AcFileStorageProjectCategory(root_path, account_id)
        self.data_objects["project-labels"] = AcFileStorageProjectLabel(root_path, account_id)
        self.data_objects["project-notes"] = AcFileStorageProjectNote(root_path, account_id)
        self.data_objects["tasks"] = AcFileStorageTask(root_path, account_id)
        self.data_objects["task-labels"] = AcFileStorageTaskLabel(root_path, account_id)
        self.data_objects["task-lists"] = AcFileStorageTaskList(root_path, account_id)

    def reset(self):
        if os.path.exists(self.root_path):
            for obj in self.data_objects.keys():
                self.data_objects[obj].reset()
            tmp_path = '%s_%d' % (self.root_path, time.time())
            os.rename(self.root_path, tmp_path)
            shutil.rmtree(tmp_path)

    def ensure_dirs(self):
        if not os.path.exists(self.get_account_path()):
            os.makedirs(self.get_account_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_subtasks_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_comments_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_attachments_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_task_history_path(), DEFAULT_MODE_DIRS)
        for obj in self.data_objects.keys():
            self.data_objects[obj].ensure_dirs()

    def get_account_path(self) -> str:
        return os.path.join(self.root_path, "account-%08d" % self.account_id)

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

