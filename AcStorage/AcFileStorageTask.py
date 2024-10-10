import json
import os
import shutil
import time

from AcStorage import DEFAULT_MODE_DIRS
from AcTask import AcTask
from ActiveCollabAPI import AC_CLASS_TASK, AC_ERROR_WRONG_CLASS


class AcFileStorageTask:
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
        return os.path.join(self.get_account_path(), "tasks")

    @staticmethod
    def get_filename(task: AcTask) -> str:
        return "task-%08d.json" % task.id

    def get_full_filename(self, task_filename: str) -> str:
        return os.path.join(self.get_path(), task_filename)

    def save(self, task: AcTask) -> str:
        assert task.class_ == AC_CLASS_TASK, AC_ERROR_WRONG_CLASS
        task_filename = self.get_filename(task)
        task_full_filename = self.get_full_filename(task_filename)
        with open(task_full_filename, "w") as f:
            json.dump(task.to_dict(), f, sort_keys=True, indent=2)
        return task_full_filename
