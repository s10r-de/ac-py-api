from typing import Iterator

from active_collab_api import AC_CLASS_TASK_LIST, AC_ERROR_WRONG_CLASS
from active_collab_api.ac_task_list import AcTaskList, task_list_from_json

from .base import AcFileStorageBaseClass


class AcFileStorageTaskList(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "task-list"
        self.dir_name = "task-lists"
        self.data: Iterator[AcTaskList] | None = None

    def setup(self):
        pass

    def save(self, task_list: AcTaskList) -> str:
        assert task_list.class_ == AC_CLASS_TASK_LIST, AC_ERROR_WRONG_CLASS
        self.data = None
        return super().save_with_id(task_list, task_list.id)

    def load(self, task_list_id: int) -> AcTaskList:
        task_list = super().load_by_id(task_list_id)
        return task_list_from_json(task_list)

    def get_all(self) -> Iterator[AcTaskList]:
        if self.data is None:
            self.data = list(map(task_list_from_json, super().get_all()))
        return self.data

    def find_by_project(self, project_id: int) -> Iterator[AcTaskList]:
        return filter(lambda task: task.project_id == project_id, self.get_all())
