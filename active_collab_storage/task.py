from typing import Iterator

from active_collab_api import AC_CLASS_TASK, AC_ERROR_WRONG_CLASS
from active_collab_api.ac_task import AcTask, task_from_json
from .base import AcFileStorageBaseClass


class AcFileStorageTask(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "task"
        self.dir_name = "tasks"
        self.data: Iterator[AcTask] | None = None

    def setup(self):
        pass

    def save(self, task: AcTask) -> str:
        assert task.class_ == AC_CLASS_TASK, AC_ERROR_WRONG_CLASS
        self.data = None
        return super().save_with_id(task, task.id)

    def load(self, task_id: int) -> AcTask:
        task = self.load_by_id(task_id)
        return task_from_json(task)

    def get_all(self) -> Iterator[AcTask]:
        if self.data is None:
            self.data = list(map(task_from_json, super().get_all()))
        return self.data

    def find_by_project(self, project_id: int) -> Iterator[AcTask]:
        return filter(lambda task: task.project_id == project_id, self.get_all())

    def find_by_tasklist(self, task_list_id: int) -> Iterator[AcTask]:
        return filter(lambda task: task.task_list_id == task_list_id, self.get_all())
