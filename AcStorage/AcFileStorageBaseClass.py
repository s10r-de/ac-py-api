import glob
import json
import locale
import os
import shutil
import time

from AcStorage import DEFAULT_MODE_DIRS


class AcFileStorageBaseClass:
    filename_prefix = None
    dir_name = None

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
        return os.path.join(self.get_account_path(), self.dir_name)

    def get_filename(self, obj, generate_id=None) -> str:
        id = obj.id
        if generate_id:
            id = generate_id(obj)
        return self.filename_with_id(id)

    def filename_with_id(self, id: int) -> str:
        return "%s-%08d.json" % (self.filename_prefix, id)

    def get_full_filename(self, task_filename: str) -> str:
        return os.path.join(self.get_path(), task_filename)

    def save(self, obj, generate_id=None) -> str:
        filename = self.get_filename(obj, generate_id)
        full_filename = self.get_full_filename(filename)
        with open(full_filename, "w") as f:
            json.dump(obj.to_dict(), f, sort_keys=True, indent=2)
        return full_filename

    def list(self) -> list[int]:
        # strip path and "${filename_prefix}-" and ".json"
        n = len(self.filename_prefix)

        def extract_number(f: str) -> int:
            return locale.atoi(os.path.basename(f)[n + 1:-5])

        return map(extract_number,
                   glob.iglob(os.path.join(self.get_path(), self.filename_prefix + "-*.json")))

    def load(self, id: int) -> dict:
        filename = self.filename_with_id(id)
        full_filename = self.get_full_filename(filename)
        return json.load(open(full_filename, "r"))
