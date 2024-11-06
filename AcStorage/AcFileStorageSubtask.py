from AcFileStorageBaseClass import AcFileStorageBaseClass
from ActiveCollabAPI.AcSubtask import AcSubtask
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS, AC_CLASS_SUBTASK


class AcFileStorageSubtask(AcFileStorageBaseClass):

    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "subtask"
        self.dir_name = "subtasks"

    def setup(self):
        pass

    def save(self, subtask: AcSubtask) -> str:
        assert subtask.class_ == AC_CLASS_SUBTASK, AC_ERROR_WRONG_CLASS
        return super().save_with_id(subtask, subtask.id)
