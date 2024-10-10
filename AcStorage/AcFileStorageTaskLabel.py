import json
import os
import shutil
import time

from AcStorage import DEFAULT_MODE_DIRS
from AcTaskLabel import AcTaskLabel
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS, AC_CLASS_TASK_LABEL


class AcFileStorageTaskLabel:
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
        return os.path.join(self.get_account_path(), "task-labels")

    @staticmethod
    def get_filename(task_label: AcTaskLabel) -> str:
        return "task-label-%08d.json" % task_label.id

    def get_full_filename(self, task_label_filename: str) -> str:
        return os.path.join(self.get_path(), task_label_filename)

    def save(self, task_label: AcTaskLabel) -> str:
        assert task_label.class_ == AC_CLASS_TASK_LABEL, AC_ERROR_WRONG_CLASS
        task_label_filename = self.get_filename(task_label)
        task_label_full_filename = self.get_full_filename(task_label_filename)
        with open(task_label_full_filename, "w") as f:
            json.dump(task_label.to_dict(), f, sort_keys=True, indent=2)
        return task_label_full_filename
