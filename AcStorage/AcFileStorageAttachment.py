import os
import shutil

from AcStorage.AcFileStorageBaseClass import AcFileStorageBaseClass
from active_collab_api import (
    AC_ERROR_WRONG_CLASS,
    AC_CLASS_ATTACHMENT_WAREHOUSE,
    AC_CLASS_ATTACHMENT_LOCAL,
)
from active_collab_api.AcAttachment import AcAttachment, attachment_from_json


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
        shutil.move(tmp_download, self.get_bin_filename(attachment))
        return attachment_full_filename

    def get_bin_filename(self, attachment):
        # FIXME: 2 lines duplicate with base class save_id()
        filename = self.filename_with_id(attachment.id)
        full_filename = self.get_full_filename(filename)
        return full_filename + "." + attachment.extension

    def load(self, attachment_id: int) -> AcAttachment:
        attachment_json = self.load_by_id(attachment_id)
        return attachment_from_json(attachment_json)
