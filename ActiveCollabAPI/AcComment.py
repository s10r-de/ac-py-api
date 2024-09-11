import dataclasses
import json
from dataclasses import dataclass


@dataclass
class AcComment:
    attachments: []
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
        d["class"] = d["class_"]
        del d["class_"]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def comment_from_json(json_obj: dict) -> AcComment:
    json_obj["class_"] = json_obj["class"]
    del json_obj["class"]
    return AcComment(**json_obj)
