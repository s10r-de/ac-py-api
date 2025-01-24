from typing import Iterator

from active_collab_api import AC_CLASS_COMMENT, AC_ERROR_WRONG_CLASS, AC_CLASS_TASK
from active_collab_api.ac_comment import AcComment, comment_from_json

from .base import AcFileStorageBaseClass


class AcFileStorageComment(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "comment"
        self.dir_name = "comments"
        self.data = None

    def setup(self):
        pass

    def save(self, comment: AcComment) -> str:
        assert comment.class_ == AC_CLASS_COMMENT, AC_ERROR_WRONG_CLASS
        self.data = None
        return super().save_with_id(comment, comment.id)

    def load(self, comment_id: int) -> AcComment:
        comment: dict = self.load_by_id(comment_id)
        return comment_from_json(comment)

    def get_all(self):
        if self.data is None:
            self.data = list(map(comment_from_json, super().get_all()))
        return self.data

    def find_by_task(self, task_id: int) -> Iterator[AcComment]:
        return filter(lambda t: t.parent_id == task_id and
                                t.parent_type == AC_CLASS_TASK,
                      self.get_all())

    def sort_by_created(self, comment: Iterator[AcComment]) -> list[AcComment]:
        return sorted(comment, key=lambda t: t.created_on)
