from ActiveCollabAPI.AcCompany import AcCompany, company_from_json
from AcStorage.AcFileStorageBaseClass import AcFileStorageBaseClass
from ActiveCollabAPI import AC_CLASS_COMPANY, AC_ERROR_WRONG_CLASS


class AcFileStorageCompany(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.dir_name = "companies"
        self.filename_prefix = "company"

    def setup(self):
        pass

    def save(self, company: AcCompany) -> str:
        assert company.class_ == AC_CLASS_COMPANY, AC_ERROR_WRONG_CLASS
        return super().save_with_id(company, company.id)

    def load(self, company_id) -> AcCompany:
        data = super().load_by_id(company_id)
        return company_from_json(data)
