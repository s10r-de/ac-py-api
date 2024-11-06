from AcFileStorageBaseClass import AcFileStorageBaseClass
from ActiveCollabAPI.AcUser import AcUser, user_from_json
from ActiveCollabAPI import AC_CLASS_USER_MEMBER, AC_CLASS_USER_OWNER, AC_ERROR_WRONG_CLASS


class AcFileStorageUser(AcFileStorageBaseClass):

    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "user"
        self.dir_name = "users"

    def setup(self):
        pass

    def save(self, user: AcUser) -> str:
        assert user.class_ == AC_CLASS_USER_MEMBER or user.class_ == AC_CLASS_USER_OWNER, AC_ERROR_WRONG_CLASS
        return super().save_with_id(user, user.id)

    def load(self, user_id: int) -> AcUser:
        data = super().load_by_id(user_id)
        return user_from_json(data)
