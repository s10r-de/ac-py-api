from active_collab_storage.AcFileStorageBaseClass import AcFileStorageBaseClass
from active_collab_api.AcSubtask import AcSubtask, subtask_from_json
from active_collab_api import AC_ERROR_WRONG_CLASS, AC_CLASS_SUBTASK


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

    def load(self, subtask_id: int) -> AcSubtask:
        subtask = self.load_by_id(subtask_id)
        return subtask_from_json(subtask)
