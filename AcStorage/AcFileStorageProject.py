from AcFileStorageBaseClass import AcFileStorageBaseClass
from ActiveCollabAPI.AcProject import AcProject, project_from_json
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

    def load(self, project_id: int) -> AcProject:
        project = self.load_by_id(project_id)
        return project_from_json(project)
