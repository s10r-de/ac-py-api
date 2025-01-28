import os
import shutil
from typing import Iterator

from active_collab_api import (
    AC_CLASS_ATTACHMENT_LOCAL,
    AC_CLASS_ATTACHMENT_WAREHOUSE,
    AC_ERROR_WRONG_CLASS,
)
from active_collab_api.ac_attachment import AcAttachment, attachment_from_json

from .base import AcFileStorageBaseClass


class AcFileStorageAttachment(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "attachment"
        self.dir_name = "attachments"
        self.data = None

    def setup(self):
        pass

    def save(self, attachment: AcAttachment, tmp_download: str) -> str:
        assert attachment.class_ in [
            AC_CLASS_ATTACHMENT_WAREHOUSE,
            AC_CLASS_ATTACHMENT_LOCAL,
        ], AC_ERROR_WRONG_CLASS
        assert os.path.exists(tmp_download)
        self.data = None
        attachment_full_filename = super().save_with_id(attachment, attachment.id)
        shutil.move(tmp_download, self.get_bin_filename(attachment))
        return attachment_full_filename

    def get_bin_filename(self, attachment: AcAttachment) -> str:
        # FIXME: 2 lines duplicate with base class save_id()
        filename = self.filename_with_id(attachment.id)
        full_filename = self.get_full_filename(filename)
        return full_filename + "." + attachment.extension

    def load(self, attachment_id: int) -> AcAttachment:
        attachment_json = self.load_by_id(attachment_id)
        return attachment_from_json(attachment_json)

    def get_all(self)-> Iterator[AcAttachment]:
        if self.data is None:
            self.data = list(map(attachment_from_json, super().get_all()))
        return self.data

    def find_by_task(self, task_id: int) -> Iterator[AcAttachment]:
        return filter(lambda t: t.parent_id == task_id and
                                t.parent_type == "Task", self.get_all())

    def find_by_comment(self, comment_id: int) -> Iterator[AcAttachment]:
        return filter(lambda t: t.parent_id == comment_id and
                                t.parent_type == "Comment", self.get_all())
