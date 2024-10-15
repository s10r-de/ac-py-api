from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcProject import AcProject
from ActiveCollabAPI import AC_CLASS_PROJECT, AC_ERROR_WRONG_CLASS


class AcFileStorageProject(AcFileStorageBaseClass):

    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "project"
        self.dir_name = "projects"

    def setup(self):
        pass

    def save(self, project: AcProject) -> str:
        assert project.class_ == AC_CLASS_PROJECT, AC_ERROR_WRONG_CLASS
        return super().save_with_id(project, project.id)
