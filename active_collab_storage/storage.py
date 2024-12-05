import os
import shutil
import time

from active_collab_storage import DEFAULT_MODE_DIRS
from .attachment import AcFileStorageAttachment
from .comment import AcFileStorageComment
from .company import AcFileStorageCompany
from .project import AcFileStorageProject
from .project_category import (
    AcFileStorageProjectCategory,
)
from .project_label import AcFileStorageProjectLabel
from .project_note import AcFileStorageProjectNote
from .subtask import AcFileStorageSubtask
from .task import AcFileStorageTask
from .task_history import AcFileStorageTaskHistory
from .task_label import AcFileStorageTaskLabel
from .task_list import AcFileStorageTaskList
from .user import AcFileStorageUser


class AcFileStorage:
    def __init__(self, root_path: str, account_id: int):
        self.root_path = root_path
        self.account_id = account_id
        self.data_objects = {
            "companies": AcFileStorageCompany(root_path, account_id),
            "users": AcFileStorageUser(root_path, account_id),
            "projects": AcFileStorageProject(root_path, account_id),
            "project-categories": AcFileStorageProjectCategory(root_path, account_id),
            "project-labels": AcFileStorageProjectLabel(root_path, account_id),
            "project-notes": AcFileStorageProjectNote(root_path, account_id),
            "tasks": AcFileStorageTask(root_path, account_id),
            "task-labels": AcFileStorageTaskLabel(root_path, account_id),
            "task-lists": AcFileStorageTaskList(root_path, account_id),
            "task-history": AcFileStorageTaskHistory(root_path, account_id),
            "subtasks": AcFileStorageSubtask(root_path, account_id),
            "comments": AcFileStorageComment(root_path, account_id),
            "attachments": AcFileStorageAttachment(root_path, account_id),
        }

    def reset(self):
        for _k, obj in self.data_objects.items():
            obj.reset()
        if os.path.exists(self.root_path):
            tmp_path = "%s_%d" % (self.root_path, time.time())
            os.rename(self.root_path, tmp_path)
            shutil.rmtree(tmp_path)

    def ensure_dirs(self):
        if not os.path.exists(self.get_account_path()):
            os.makedirs(self.get_account_path(), DEFAULT_MODE_DIRS)
        for _k, obj in self.data_objects.items():
            obj.ensure_dirs()

    def get_account_path(self) -> str:
        return os.path.join(self.root_path, "account-%08d" % self.account_id)
