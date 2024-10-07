import json
import os
import shutil
import time

from AcStorage import DEFAULT_MODE_DIRS
from AcTaskList import AcTaskList
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS, AC_CLASS_TASK_LIST


class AcFileStorageTaskList:
    def __init__(self, root_path: str, account_id: int):
        self.root_path = root_path
        self.account_id = account_id

    def reset(self):
        if os.path.exists(self.get_path()):
            tmp_path = '%s_%d' % (self.get_path(), time.time())
            os.rename(self.get_path(), tmp_path)
            shutil.rmtree(tmp_path)

    def ensure_dirs(self):
        if not os.path.exists(self.get_path()):
            os.makedirs(self.get_path(), DEFAULT_MODE_DIRS)

    def get_account_path(self) -> str:
        return os.path.join(self.root_path, "account-%08d" % self.account_id)

    def get_path(self) -> str:
        return os.path.join(self.get_account_path(), "task-lists")

    @staticmethod
    def get_filename(task_label: AcTaskList) -> str:
        return "task-list-%08d.json" % task_label.id

    def get_full_filename(self, task_label_filename: str) -> str:
        return os.path.join(self.get_path(), task_label_filename)

    def save(self, task_list: AcTaskList) -> str:
        assert task_list.class_ == AC_CLASS_TASK_LIST, AC_ERROR_WRONG_CLASS
        task_list_filename = self.get_filename(task_list)
        task_list_full_filename = self.get_full_filename(task_list_filename)
        with open(task_list_full_filename, "w") as f:
            json.dump(task_list.to_dict(), f, sort_keys=True, indent=2)
        return task_list_full_filename
