from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcProjectLabel import AcProjectLabel
from ActiveCollabAPI import AC_CLASS_PROJECT_LABEL, AC_ERROR_WRONG_CLASS


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
