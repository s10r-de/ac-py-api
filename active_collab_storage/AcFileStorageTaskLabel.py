from active_collab_api import AC_CLASS_TASK_LABEL, AC_ERROR_WRONG_CLASS
from active_collab_api.ac_task_label import AcTaskLabel

from active_collab_storage.AcFileStorageBaseClass import AcFileStorageBaseClass


class AcFileStorageTaskLabel(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "task-label"
        self.dir_name = "task-labels"

    def setup(self):
        pass

    def save(self, task_label: AcTaskLabel) -> str:
        assert task_label.class_ == AC_CLASS_TASK_LABEL, AC_ERROR_WRONG_CLASS
        return super().save_with_id(task_label, task_label.id)
