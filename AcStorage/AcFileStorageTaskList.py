from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcTaskList import AcTaskList
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS, AC_CLASS_TASK_LIST


class AcFileStorageTaskList(AcFileStorageBaseClass):

    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "task-list"
        self.dir_name = "task-lists"

    def setup(self):
        pass

    def save(self, task_list: AcTaskList) -> str:
        assert task_list.class_ == AC_CLASS_TASK_LIST, AC_ERROR_WRONG_CLASS
        return super().save_with_id(task_list, task_list.id)
