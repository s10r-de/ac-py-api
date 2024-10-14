from AcCompany import AcCompany, company_from_json
from AcFileStorageBaseClass import AcFileStorageBaseClass
from ActiveCollabAPI import AC_CLASS_COMPANY, AC_ERROR_WRONG_CLASS


class AcFileStorageCompany(AcFileStorageBaseClass):
    filename_prefix = "comment"
    dir_name = "comments"

    def save(self, company: AcCompany) -> str:
        assert company.class_ == AC_CLASS_COMPANY, AC_ERROR_WRONG_CLASS
        return super().save_with_id(company, company.id)

    def load(self, company_id) -> AcCompany:
        data = super().load(company_id)
        return company_from_json(data)
