from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcSubtask import AcSubtask
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS, AC_CLASS_SUBTASK


class AcFileStorageSubtask(AcFileStorageBaseClass):
    filename_prefix = "subtask"
    dir_name = "subtasks"

    def save(self, subtask: AcSubtask) -> str:
        assert subtask.class_ == AC_CLASS_SUBTASK, AC_ERROR_WRONG_CLASS
        return super().save_with_id(subtask, subtask.id)
