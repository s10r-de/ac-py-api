import dataclasses
import json
from dataclasses import dataclass

from active_collab_api import (
    AC_CLASS_ATTACHMENT_WAREHOUSE,
    AC_PROPERTY_CLASS,
    AC_PROPERTY_CLASS_,
    AC_CLASS_ATTACHMENT_LOCAL,
    AC_ERROR_WRONG_CLASS,
)


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
    file_meta: list  # FIXME
    created_on: int
    created_by_id: int
    created_by_name: str
    created_by_email: str
    updated_on: int
    updated_by_id: int
    folder_id: int  # == project_id ?
    disposition: str
    project_id: int
    is_hidden_from_clients: bool
    extension: str
    file_type: str
    type: str | None = dataclasses.field(default=None)

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        if d["extension"] is None:
            d["extension"] = "none"
        d["extension"] = d["extension"].lower()
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def get_bin_filename(self) -> str:
        pass


def attachment_from_json(json_obj: dict) -> AcAttachment:
    assert (
        json_obj[AC_PROPERTY_CLASS] == AC_CLASS_ATTACHMENT_WAREHOUSE
        or json_obj[AC_PROPERTY_CLASS] == AC_CLASS_ATTACHMENT_LOCAL
    ), AC_ERROR_WRONG_CLASS
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    if json_obj["extension"] is None:
        json_obj["extension"] = "none"
    json_obj["extension"] = json_obj["extension"].lower()
    return AcAttachment(**json_obj)
