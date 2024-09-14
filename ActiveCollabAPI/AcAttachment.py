import dataclasses
import json
from dataclasses import dataclass


@dataclass
class AcAttachment:
    id: int
    class_: str
    url_path: str
    name: str
    parent_type: str
    parent_id: int
    mime_type: str
    size: int
    md5: str
    thumbnail_url: str
    preview_url: str
    download_url: str
    file_meta: []  # FIXME
    created_on: int
    created_by_id: int
    created_by_name: str
    created_by_email: str
    updated_on: int
    updated_by_id: int
    folder_id: int
    disposition: str
    project_id: int
    is_hidden_from_clients: bool
    extension: str
    file_type: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d["class"] = d["class_"]
        del d["class_"]
        if d['extension'] is None:
            d['extension'] = 'none'
        d['extension'] = d['extension'].lower()
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def attachment_from_json(json_obj: dict) -> AcAttachment:
    json_obj["class_"] = json_obj["class"]
    del json_obj["class"]
    if json_obj["extension"] is None:
        json_obj["extension"] = "none"
    json_obj["extension"] = json_obj["extension"].lower()
    return AcAttachment(**json_obj)
