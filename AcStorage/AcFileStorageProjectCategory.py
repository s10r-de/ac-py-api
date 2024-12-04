from AcStorage.AcFileStorageBaseClass import AcFileStorageBaseClass
from active_collab_api.AcProjectCategory import (
    AcProjectCategory,
    project_category_from_json,
)
from active_collab_api import AC_CLASS_PROJECT_CATEGORY, AC_ERROR_WRONG_CLASS


class AcFileStorageProjectCategory(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "project-category"
        self.dir_name = "project-categories"

    def setup(self):
        pass

    def save(self, project_category: AcProjectCategory) -> str:
        assert (
            project_category.class_ == AC_CLASS_PROJECT_CATEGORY
        ), AC_ERROR_WRONG_CLASS
        return super().save_with_id(project_category, project_category.id)

    def load(self, project_category_id) -> AcProjectCategory:
        data = super().load_by_id(project_category_id)
        return project_category_from_json(data)
