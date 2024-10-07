import json
import os
import shutil
import time

from AcStorage import DEFAULT_MODE_DIRS
from AcUser import AcUser
from ActiveCollabAPI import AC_CLASS_USER_MEMBER, AC_CLASS_USER_OWNER, AC_ERROR_WRONG_CLASS


class AcFileStorageUser:
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
        return os.path.join(self.get_account_path(), "users")

    @staticmethod
    def get_filename(user: AcUser) -> str:
        return "user-%08d.json" % user.id

    def get_full_filename(self, user_filename: str) -> str:
        return os.path.join(self.get_path(), user_filename)

    def save(self, user: AcUser) -> str:
        assert user.class_ == AC_CLASS_USER_MEMBER or user.class_ == AC_CLASS_USER_OWNER, AC_ERROR_WRONG_CLASS
        user_filename = self.get_filename(user)
        user_full_filename = self.get_full_filename(user_filename)
        with open(user_full_filename, "w") as f:
            json.dump(user.to_dict(), f, sort_keys=True, indent=2)
        return user_full_filename
