import json
import os
import shutil
import time

from AcCompany import AcCompany
from AcStorage import DEFAULT_MODE_DIRS
from ActiveCollabAPI import AC_CLASS_COMPANY, AC_ERROR_WRONG_CLASS


class AcFileStorageCompany:
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
        return os.path.join(self.get_account_path(), "companies")

    @staticmethod
    def get_filename(company: AcCompany) -> str:
        return "company-%08d.json" % company.id

    def get_full_filename(self, company_filename: str) -> str:
        return os.path.join(self.get_path(), company_filename)

    def save(self, company: AcCompany) -> str:
        assert company.class_ == AC_CLASS_COMPANY, AC_ERROR_WRONG_CLASS
        company_filename = self.get_filename(company)
        company_full_filename = self.get_full_filename(company_filename)
        with open(company_full_filename, "w") as f:
            json.dump(company.to_dict(), f, sort_keys=True, indent=2)
        return company_full_filename
