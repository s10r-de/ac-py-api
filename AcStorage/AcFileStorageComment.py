from ActiveCollabAPI.AcComment import AcComment, comment_from_json
from AcFileStorageBaseClass import AcFileStorageBaseClass
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS, AC_CLASS_COMMENT


class AcFileStorageComment(AcFileStorageBaseClass):

    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "comment"
        self.dir_name = "comments"

    def setup(self):
        pass

    def save(self, comment: AcComment) -> str:
        assert comment.class_ == AC_CLASS_COMMENT, AC_ERROR_WRONG_CLASS
        return super().save_with_id(comment, comment.id)

    def load(self, comment_id: int) -> AcComment:
        comment = self.load_by_id(comment_id)
        return comment_from_json(comment)
