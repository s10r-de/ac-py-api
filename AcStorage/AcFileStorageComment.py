import json
import os
import shutil
import time

from AcComment import AcComment
from AcStorage import DEFAULT_MODE_DIRS
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS, AC_CLASS_COMMENT


class AcFileStorageComment:
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
        return os.path.join(self.get_account_path(), "comments")

    @staticmethod
    def get_filename(comment: AcComment) -> str:
        return "comment-%08d.json" % comment.id

    def get_full_filename(self, task_filename: str) -> str:
        return os.path.join(self.get_path(), task_filename)

    def save(self, comment: AcComment) -> str:
        assert comment.class_ == AC_CLASS_COMMENT, AC_ERROR_WRONG_CLASS
        comment_filename = self.get_filename(comment)
        comment_full_filename = self.get_full_filename(comment_filename)
        with open(comment_full_filename, "w") as f:
            json.dump(comment.to_dict(), f, sort_keys=True, indent=2)
        return comment_full_filename
