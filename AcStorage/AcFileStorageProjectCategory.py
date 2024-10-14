from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcProjectCategory import AcProjectCategory
from ActiveCollabAPI import AC_CLASS_PROJECT_CATEGORY, AC_ERROR_WRONG_CLASS


class AcFileStorageProjectCategory(AcFileStorageBaseClass):

    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "project-category"
        self.dir_name = "project-categories"

    def setup(self):
        pass

    def save(self, project_category: AcProjectCategory) -> str:
        assert project_category.class_ == AC_CLASS_PROJECT_CATEGORY, AC_ERROR_WRONG_CLASS
        return super().save_with_id(project_category, project_category.id)
