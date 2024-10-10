import json
import os
import shutil
import time

from AcAttachment import AcAttachment
from AcStorage import DEFAULT_MODE_DIRS
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS, AC_CLASS_ATTACHMENT_WAREHOUSE


class AcFileStorageAttachment:
    def __init__(self, root_path: str, account_id: int):
        self.root_path = root_path
        self.account_id = account_id

    def reset(self):
        if os.path.exists(self.get_path()):
            tmp_path = '%s_%d' % (self.get_path(), time.time())
            os.rename(self.get_path(), tmp_path)
            shutil.rmtree(tmp_path)

    def ensure_dirs(self):
        if not os.path.exists(self.get_path()):
            os.makedirs(self.get_path(), DEFAULT_MODE_DIRS)

    def get_account_path(self) -> str:
        return os.path.join(self.root_path, "account-%08d" % self.account_id)

    def get_path(self) -> str:
        return os.path.join(self.get_account_path(), "attachments")

    @staticmethod
    def get_filename(comment: AcAttachment) -> str:
        return "attachment-%08d.json" % comment.id

    def get_full_filename(self, task_filename: str) -> str:
        return os.path.join(self.get_path(), task_filename)

    def save(self, attachment: AcAttachment, tmp_download: str) -> str:
        assert attachment.class_ == AC_CLASS_ATTACHMENT_WAREHOUSE, AC_ERROR_WRONG_CLASS
        attachment_filename = self.get_filename(attachment)
        attachment_full_filename = self.get_full_filename(attachment_filename)
        with open(attachment_full_filename, "w") as f:
            json.dump(attachment.to_dict(), f, sort_keys=True, indent=2)
        shutil.move(tmp_download, attachment_full_filename + '.' + attachment.extension)
        return attachment_full_filename
