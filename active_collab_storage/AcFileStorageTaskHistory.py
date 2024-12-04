from active_collab_storage.AcFileStorageBaseClass import AcFileStorageBaseClass
from active_collab_api.AcTaskHistory import AcTaskHistory


class AcFileStorageTaskHistory(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "task-history"
        self.dir_name = "task-history"

    def setup(self):
        pass

    @staticmethod
    def make_id(task_id, timestamp) -> int:
        return task_id * 10000000000 + timestamp

    def save(self, task_history: AcTaskHistory) -> str:
        obj_id = self.make_id(task_history.task_id, task_history.timestamp)
        return super().save_with_id(task_history, obj_id)
