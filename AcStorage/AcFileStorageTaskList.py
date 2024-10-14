from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcTaskList import AcTaskList
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS, AC_CLASS_TASK_LIST


class AcFileStorageTaskList(AcFileStorageBaseClass):
    filename_prefix = "task-list"
    dir_name = "task-lists"

    def save(self, task_list: AcTaskList) -> str:
        assert task_list.class_ == AC_CLASS_TASK_LIST, AC_ERROR_WRONG_CLASS
        return super().save_with_id(task_list, task_list.id)
