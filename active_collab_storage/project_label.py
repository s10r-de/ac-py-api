from active_collab_api import AC_CLASS_PROJECT_LABEL, AC_ERROR_WRONG_CLASS
from active_collab_api.ac_project_label import AcProjectLabel, project_label_from_json

from .base import AcFileStorageBaseClass


class AcFileStorageProjectLabel(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "project-label"
        self.dir_name = "project-labels"

    def setup(self):
        pass

    def save(self, project_label: AcProjectLabel) -> str:
        assert project_label.class_ == AC_CLASS_PROJECT_LABEL, AC_ERROR_WRONG_CLASS
        return super().save_with_id(project_label, project_label.id)

    def load(self, project_label_id: int) -> AcProjectLabel:
        data = super().load_by_id(project_label_id)
        return project_label_from_json(data)
