from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcUser import AcUser, user_from_json
from ActiveCollabAPI import AC_CLASS_USER_MEMBER, AC_CLASS_USER_OWNER, AC_ERROR_WRONG_CLASS


class AcFileStorageUser(AcFileStorageBaseClass):
    filename_prefix = "user"
    dir_name = "users"

    def save(self, user: AcUser) -> str:
        assert user.class_ == AC_CLASS_USER_MEMBER or user.class_ == AC_CLASS_USER_OWNER, AC_ERROR_WRONG_CLASS
        return super().save(user)

    def load(self, user_id: int) -> AcUser:
        data = super().load(user_id)
        return user_from_json(data)
