import glob
import json
import locale
import os
import shutil
import time

from AcStorage import DEFAULT_MODE_DIRS, AC_ERROR_ID_MUST_BE_INT


class AcFileStorageBaseClass:

    def __init__(self, root_path: str, account_id: int):
        self.dir_name = ""
        self.filename_prefix = ""
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
        return os.path.join(self.get_account_path(), self.dir_name)

    def filename_with_id(self, id: int) -> str:
        assert isinstance(id, int), AC_ERROR_ID_MUST_BE_INT
        return "%s-%018d.json" % (self.filename_prefix, id)

    def get_full_filename(self, task_filename: str) -> str:
        return os.path.join(self.get_path(), task_filename)

    def save_with_id(self, obj, id) -> str:
        filename = self.filename_with_id(id)
        full_filename = self.get_full_filename(filename)
        with open(full_filename, "w") as f:
            json.dump(obj.to_dict(), f, sort_keys=True, indent=2)
        return full_filename

    def list_ids(self) -> list[int]:
        # strip path and "${filename_prefix}-" and ".json" to get the ID for the object
        n = len(self.filename_prefix)

        def extract_id(f: str) -> int:
            return locale.atoi(os.path.basename(f)[n + 1:-5])

        ids = list(map(extract_id,
                       glob.iglob(os.path.join(self.get_path(),
                                               self.filename_prefix + "-*.json"))))
        ids.sort()
        return ids

    def load_by_id(self, id: int) -> dict:
        filename = self.filename_with_id(id)
        full_filename = self.get_full_filename(filename)
        with open(full_filename, "r") as f:
            data = json.load(f)
        return data
