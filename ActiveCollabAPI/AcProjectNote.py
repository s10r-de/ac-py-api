import dataclasses
import json
from dataclasses import dataclass

from AcAttachment import AcAttachment, attachment_from_json
from ActiveCollabAPI import AC_CLASS_PROJECT_NOTE, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_, AC_ERROR_WRONG_CLASS


@dataclass
class AcProjectNote:
    id: int
    class_: str
    url_path: str
    name: str
    comments_count: int
    attachments: [AcAttachment]
    is_trashed: bool
    trashed_on: int | None
    trashed_by_id: int
    project_id: int
    is_hidden_from_clients: bool
    body: str
    body_formatted: str
    body_mode: str
    body_plain_text: str
    created_on: int
    created_by_id: int
    created_by_name: str
    created_by_email: str
    updated_on: int
    updated_by_id: int
    notebook_id: int
    note_group_id: int
    in_notebook: bool
    is_pinned: bool
    position: int
    contributor_ids: [int]

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def project_note_from_json(json_obj: dict) -> AcProjectNote:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_PROJECT_NOTE, AC_ERROR_WRONG_CLASS
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    json_obj["attachments"] = list(map(lambda a: attachment_from_json(a), json_obj["attachments"]))
    return AcProjectNote(**json_obj)
