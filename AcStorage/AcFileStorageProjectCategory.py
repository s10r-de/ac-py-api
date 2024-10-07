import json
import os
import shutil
import time

from AcProjectCategory import AcProjectCategory
from AcStorage import DEFAULT_MODE_DIRS
from ActiveCollabAPI import AC_CLASS_PROJECT_CATEGORY, AC_ERROR_WRONG_CLASS


class AcFileStorageProjectCategory:
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
        return os.path.join(self.get_account_path(), "project-categories")

    @staticmethod
    def get_filename(project: AcProjectCategory) -> str:
        return "project-category-%08d.json" % project.id

    def get_full_filename(self, project_filename: str) -> str:
        return os.path.join(self.get_path(), project_filename)

    def save(self, project_category: AcProjectCategory) -> str:
        assert project_category.class_ == AC_CLASS_PROJECT_CATEGORY, AC_ERROR_WRONG_CLASS
        project_category_filename = self.get_filename(project_category)
        project_category_full_filename = self.get_full_filename(project_category_filename)
        with open(project_category_full_filename, "w") as f:
            json.dump(project_category.to_dict(), f, sort_keys=True, indent=2)
        return project_category_full_filename
