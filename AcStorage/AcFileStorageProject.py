from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcProject import AcProject
from ActiveCollabAPI import AC_CLASS_PROJECT, AC_ERROR_WRONG_CLASS


class AcFileStorageProject(AcFileStorageBaseClass):
    filename_prefix = "project"
    dir_name = "projects"

    def save(self, project: AcProject) -> str:
        assert project.class_ == AC_CLASS_PROJECT, AC_ERROR_WRONG_CLASS
        return super().save_with_id(project, project.id)
