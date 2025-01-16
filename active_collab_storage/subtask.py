from typing import Iterator

from active_collab_api import AC_CLASS_SUBTASK, AC_ERROR_WRONG_CLASS
from active_collab_api.ac_subtask import AcSubtask, subtask_from_json
from .base import AcFileStorageBaseClass


class AcFileStorageSubtask(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "subtask"
        self.dir_name = "subtasks"
        self.data = None

    def setup(self):
        pass

    def save(self, subtask: AcSubtask) -> str:
        assert subtask.class_ == AC_CLASS_SUBTASK, AC_ERROR_WRONG_CLASS
        self.data = None
        return super().save_with_id(subtask, subtask.id)

    def load(self, subtask_id: int) -> AcSubtask:
        subtask = self.load_by_id(subtask_id)
        return subtask_from_json(subtask)

    def get_all(self):
        if self.data is None:
            self.data = list(map(subtask_from_json, super().get_all()))
        return self.data

    def find_by_task(self, task_id: int) -> Iterator[AcSubtask]:
        return filter(lambda t: t.task_id == task_id, self.get_all())

    def sort_by_position(self, subtasks: Iterator[AcSubtask]) -> Iterator[AcSubtask]:
        return sorted(subtasks, key=lambda t: t.position)
