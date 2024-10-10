import dataclasses
import json
from dataclasses import dataclass

from AcAttachment import AcAttachment, attachment_from_json
from ActiveCollabAPI import AC_CLASS_COMMENT, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_, AC_ERROR_WRONG_CLASS


@dataclass
class AcComment:
    attachments: [AcAttachment | None]
    body: str
    body_formatted: str
    body_mode: str
    body_plain_text: str
    class_: str
    created_by_email: str
    created_by_id: int
    created_by_name: str
    created_on: int
    id: int
    is_trashed: bool
    last_modification_by_email: str | None
    last_modification_by_id: int | None
    last_modification_by_name: str | None
    last_modification_on: int | None
    parent_id: int
    parent_type: str
    project_id: int
    reactions: []
    trashed_by_id: int
    trashed_on: int | None
    updated_by_id: int
    updated_on: int
    url_path: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        if d["attachments"] is not None:
            d["attachments"] = list(map(lambda a: a.to_dict(), self.get_attachments()))
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def get_attachments(self) -> list[AcAttachment]:
        return self.attachments


def comment_from_json(json_obj: dict) -> AcComment:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_COMMENT, AC_ERROR_WRONG_CLASS
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    if json_obj["attachments"] is not None:
        json_obj["attachments"] = list(map(attachment_from_json, json_obj["attachments"]))
    return AcComment(**json_obj)
