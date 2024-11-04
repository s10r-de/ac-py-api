import dataclasses
import json
import logging
from dataclasses import dataclass

from AcDataObject import AcDataObject
from ActiveCollabAPI import AC_CLASS_USER_MEMBER, AC_CLASS_USER_OWNER, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_

AC_CLOUD_LANG_ID_GERMAN = 5
AC_CLOUD_LANG_ID_ENGLISH = 26

AC_SELFHOSTED_LANG_ID_ENGLISH = 1
AC_SELFHOSTED_LANG_ID_GERMAN = 4


@dataclass
class AcUser(AcDataObject):
    additional_email_addresses: []
    avatar_url: str
    class_: str
    company_id: int
    created_by_email: str
    created_by_id: int
    created_by_name: str
    created_on: int
    custom_permissions: []
    daily_capacity: int | None
    display_name: str
    email: str
    first_login_on: int
    first_name: str
    id: int
    im_handle: str | None
    im_type: str | None
    is_archived: bool
    is_authenticator_validated: bool
    is_email_at_example: bool
    is_pending_activation: bool
    is_trashed: bool
    language_id: int
    last_name: str
    phone: str | None
    short_display_name: str
    title: str | None
    trashed_by_id: int
    trashed_on: int
    updated_on: int
    url_path: str
    workspace_count: int
    avatar_version: str = dataclasses.field(default="")
    has_custom_avatar: bool = dataclasses.field(default=False)

    def __eq__(self, other) -> bool:
        ignored_fields = ["avatar_url", "avatar_version", "has_custom_avatar"]
        result = True
        this_data = self.to_dict()
        other_data = other.to_dict()
        for key in this_data.keys():
            if key in ignored_fields:
                continue
            this_value = this_data[key]
            other_value = other_data[key]
            if this_value != other_value:
                logging.error(
                    "AcUser[%d]: %s '%s'!='%s' - does not match -> FAIL" % (self.id, key, this_value, other_value))
                result = False
            else:
                logging.debug("AcUser[%d]: %s ='%s' - matches -> OK" % (self.id, key, this_value))
        return result

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def user_from_json(json_obj: dict) -> AcUser:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_USER_MEMBER or json_obj[AC_PROPERTY_CLASS] == AC_CLASS_USER_OWNER
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    return AcUser(**json_obj)


def map_cloud_user_language_id(user: AcUser) -> AcUser:
    """
    Workaround for language lookup tables are not in sync between cloud and self-hosted.

    If language is set to german, then adapt the ID, for any other language
    fallback to english.

    Note: you need to call this funktion only if the data is dumped from cloud
    and not from self-hosted!

    Tasks#65 https://app.activecollab.com/416910/projects/604?modal=Task-24391-604

    :param user: Original AcUser Object
    :return: the modified AcUser Object
    """
    if user.language_id == AC_CLOUD_LANG_ID_GERMAN:
        user.language_id = AC_SELFHOSTED_LANG_ID_GERMAN
    else:
        user.language_id = AC_SELFHOSTED_LANG_ID_ENGLISH
    return user
