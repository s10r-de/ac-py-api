import glob
import locale
import os

from AcCompany import AcCompany, company_from_json
from AcFileStorageBaseClass import AcFileStorageBaseClass
from ActiveCollabAPI import AC_CLASS_COMPANY, AC_ERROR_WRONG_CLASS


class AcFileStorageCompany(AcFileStorageBaseClass):
    filename_prefix = "company"
    dir_name = "companies"

    def save(self, company: AcCompany) -> str:
        assert company.class_ == AC_CLASS_COMPANY, AC_ERROR_WRONG_CLASS
        return super().save(company)

    def list(self):
        # strip path and "company-" and ".json"
        return map(lambda f: locale.atoi(os.path.basename(f)[8:-5]),
                   glob.iglob(os.path.join(self.get_path(), "company-*.json")))

    def load(self, company_id) -> AcCompany:
        data = super().load(company_id)
        return company_from_json(data)
