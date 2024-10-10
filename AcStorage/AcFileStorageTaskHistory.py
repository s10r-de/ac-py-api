import json
import os
import shutil
import time

from AcStorage import DEFAULT_MODE_DIRS
from AcTaskHistory import AcTaskHistory


class AcFileStorageTaskHistory:
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
        return os.path.join(self.get_account_path(), "task-history")

    @staticmethod
    def get_filename(task_history: AcTaskHistory) -> str:
        return "task-history-%08d-%010d.json" % (task_history.task_id, task_history.timestamp)

    def get_full_filename(self, task_history_filename: str) -> str:
        return os.path.join(self.get_path(), task_history_filename)

    def save(self, task_history: AcTaskHistory) -> str:
        task_history_filename = self.get_filename(task_history)
        task_history_full_filename = self.get_full_filename(task_history_filename)
        with open(task_history_full_filename, "w") as f:
            json.dump(task_history.to_dict(), f, sort_keys=True, indent=2)
        return task_history_full_filename
