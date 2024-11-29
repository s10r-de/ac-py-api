from AcStorage.AcFileStorageBaseClass import AcFileStorageBaseClass
from ActiveCollabAPI.AcTask import AcTask, task_from_json
from ActiveCollabAPI import AC_CLASS_TASK, AC_ERROR_WRONG_CLASS


class AcFileStorageTask(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "task"
        self.dir_name = "tasks"

    def setup(self):
        pass

    def save(self, task: AcTask) -> str:
        assert task.class_ == AC_CLASS_TASK, AC_ERROR_WRONG_CLASS
        return super().save_with_id(task, task.id)

    def load(self, task_id: int) -> AcTask:
        task = self.load_by_id(task_id)
        return task_from_json(task)
