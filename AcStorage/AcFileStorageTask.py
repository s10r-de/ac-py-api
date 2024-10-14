from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcTask import AcTask
from ActiveCollabAPI import AC_CLASS_TASK, AC_ERROR_WRONG_CLASS


class AcFileStorageTask(AcFileStorageBaseClass):
    filename_prefix = "task"
    dir_name = "tasks"

    def save(self, task: AcTask) -> str:
        assert task.class_ == AC_CLASS_TASK, AC_ERROR_WRONG_CLASS
        return super().save_with_id(task, task.id)
