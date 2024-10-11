from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcProjectCategory import AcProjectCategory
from ActiveCollabAPI import AC_CLASS_PROJECT_CATEGORY, AC_ERROR_WRONG_CLASS


class AcFileStorageProjectCategory(AcFileStorageBaseClass):
    filename_prefix = "project-category"
    dir_name = "project-categories"

    def save(self, project_category: AcProjectCategory, generate_id=None) -> str:
        assert project_category.class_ == AC_CLASS_PROJECT_CATEGORY, AC_ERROR_WRONG_CLASS
        return super().save(project_category)
