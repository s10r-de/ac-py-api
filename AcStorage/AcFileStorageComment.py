from AcComment import AcComment
from AcFileStorageBaseClass import AcFileStorageBaseClass
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS, AC_CLASS_COMMENT


class AcFileStorageComment(AcFileStorageBaseClass):
    filename_prefix = "comment"
    dir_name = "comments"

    def save(self, comment: AcComment) -> str:
        assert comment.class_ == AC_CLASS_COMMENT, AC_ERROR_WRONG_CLASS
        return super().save_with_id(comment, comment.id)
