import os
import shutil

from ActiveCollabAPI.AcAttachment import AcAttachment, attachment_from_json
from AcFileStorageBaseClass import AcFileStorageBaseClass
from ActiveCollabAPI import (
    AC_ERROR_WRONG_CLASS,
    AC_CLASS_ATTACHMENT_WAREHOUSE,
    AC_CLASS_ATTACHMENT_LOCAL,
)


class AcFileStorageAttachment(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "attachment"
        self.dir_name = "attachments"

    def setup(self):
        pass

    def save(self, attachment: AcAttachment, tmp_download: str) -> str:
        assert (
            attachment.class_ == AC_CLASS_ATTACHMENT_WAREHOUSE
            or attachment.class_ == AC_CLASS_ATTACHMENT_LOCAL
        ), AC_ERROR_WRONG_CLASS
        assert os.path.exists(tmp_download)
        attachment_full_filename = super().save_with_id(attachment, attachment.id)
        shutil.move(tmp_download, attachment_full_filename +
                    "." + attachment.extension)
        return attachment_full_filename

    def load(self, task_id: int) -> AcAttachment:
        task = self.load_by_id(task_id)
        return attachment_from_json(task)
