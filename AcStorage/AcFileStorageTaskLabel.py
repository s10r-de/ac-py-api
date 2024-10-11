from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcTaskLabel import AcTaskLabel
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS, AC_CLASS_TASK_LABEL


class AcFileStorageTaskLabel(AcFileStorageBaseClass):
    filename_prefix = "task-label"
    dir_name = "task-labels"

    def save(self, task_label: AcTaskLabel) -> str:
        assert task_label.class_ == AC_CLASS_TASK_LABEL, AC_ERROR_WRONG_CLASS
        return super().save(task_label)
