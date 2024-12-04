import os
import shutil
import time

from AcStorage import DEFAULT_MODE_DIRS
from AcStorage.AcFileStorageAttachment import AcFileStorageAttachment
from AcStorage.AcFileStorageComment import AcFileStorageComment
from AcStorage.AcFileStorageCompany import AcFileStorageCompany
from AcStorage.AcFileStorageProject import AcFileStorageProject
from AcStorage.AcFileStorageProjectCategory import AcFileStorageProjectCategory
from AcStorage.AcFileStorageProjectLabel import AcFileStorageProjectLabel
from AcStorage.AcFileStorageProjectNote import AcFileStorageProjectNote
from AcStorage.AcFileStorageSubtask import AcFileStorageSubtask
from AcStorage.AcFileStorageTask import AcFileStorageTask
from AcStorage.AcFileStorageTaskHistory import AcFileStorageTaskHistory
from AcStorage.AcFileStorageTaskLabel import AcFileStorageTaskLabel
from AcStorage.AcFileStorageTaskList import AcFileStorageTaskList
from AcStorage.AcFileStorageUser import AcFileStorageUser


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
        for obj in self.data_objects.keys():
            self.data_objects[obj].reset()
        if os.path.exists(self.root_path):
            tmp_path = "%s_%d" % (self.root_path, time.time())
            os.rename(self.root_path, tmp_path)
            shutil.rmtree(tmp_path)

    def ensure_dirs(self):
        if not os.path.exists(self.get_account_path()):
            os.makedirs(self.get_account_path(), DEFAULT_MODE_DIRS)
        for obj in self.data_objects.keys():
            self.data_objects[obj].ensure_dirs()

    def get_account_path(self) -> str:
        return os.path.join(self.root_path, "account-%08d" % self.account_id)
