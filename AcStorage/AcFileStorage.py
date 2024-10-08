import os
import shutil
import time

from AcFileStorageAttachment import AcFileStorageAttachment
from AcFileStorageComment import AcFileStorageComment
from AcFileStorageCompany import AcFileStorageCompany
from AcFileStorageProject import AcFileStorageProject
from AcFileStorageProjectCategory import AcFileStorageProjectCategory
from AcFileStorageProjectLabel import AcFileStorageProjectLabel
from AcFileStorageProjectNote import AcFileStorageProjectNote
from AcFileStorageSubtask import AcFileStorageSubtask
from AcFileStorageTask import AcFileStorageTask
from AcFileStorageTaskHistory import AcFileStorageTaskHistory
from AcFileStorageTaskLabel import AcFileStorageTaskLabel
from AcFileStorageTaskList import AcFileStorageTaskList
from AcFileStorageUser import AcFileStorageUser
from AcStorage import DEFAULT_MODE_DIRS


class AcFileStorage:

    def __init__(self, root_path: str, account_id: int):
        self.root_path = root_path
        self.account_id = account_id
        self.data_objects = {}
        self.data_objects["companies"] = AcFileStorageCompany(root_path, account_id)
        self.data_objects["users"] = AcFileStorageUser(root_path, account_id)
        self.data_objects["projects"] = AcFileStorageProject(root_path, account_id)
        self.data_objects["project-categories"] = AcFileStorageProjectCategory(root_path, account_id)
        self.data_objects["project-labels"] = AcFileStorageProjectLabel(root_path, account_id)
        self.data_objects["project-notes"] = AcFileStorageProjectNote(root_path, account_id)
        self.data_objects["tasks"] = AcFileStorageTask(root_path, account_id)
        self.data_objects["task-labels"] = AcFileStorageTaskLabel(root_path, account_id)
        self.data_objects["task-lists"] = AcFileStorageTaskList(root_path, account_id)
        self.data_objects["task-history"] = AcFileStorageTaskHistory(root_path, account_id)
        self.data_objects["subtasks"] = AcFileStorageSubtask(root_path, account_id)
        self.data_objects["comments"] = AcFileStorageComment(root_path, account_id)
        self.data_objects["attachments"] = AcFileStorageAttachment(root_path, account_id)

    def reset(self):
        for obj in self.data_objects.keys():
            self.data_objects[obj].reset()
        if os.path.exists(self.root_path):
            tmp_path = '%s_%d' % (self.root_path, time.time())
            os.rename(self.root_path, tmp_path)
            shutil.rmtree(tmp_path)

    def ensure_dirs(self):
        if not os.path.exists(self.get_account_path()):
            os.makedirs(self.get_account_path(), DEFAULT_MODE_DIRS)
        for obj in self.data_objects.keys():
            self.data_objects[obj].ensure_dirs()

    def get_account_path(self) -> str:
        return os.path.join(self.root_path, "account-%08d" % self.account_id)
