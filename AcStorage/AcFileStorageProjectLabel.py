from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcProjectLabel import AcProjectLabel
from ActiveCollabAPI import AC_CLASS_PROJECT_LABEL, AC_ERROR_WRONG_CLASS


class AcFileStorageProjectLabel(AcFileStorageBaseClass):
    filename_prefix = "project-label"
    dir_name = "project-labels"

    def save(self, project_label: AcProjectLabel, generate_id=None) -> str:
        assert project_label.class_ == AC_CLASS_PROJECT_LABEL, AC_ERROR_WRONG_CLASS
        return super().save(project_label)
