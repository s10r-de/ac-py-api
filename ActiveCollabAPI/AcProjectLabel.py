import dataclasses
import json
from dataclasses import dataclass

from ActiveCollabAPI import AC_CLASS_PROJECT_LABEL, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


@dataclass
class AcProjectLabel:
    id: int
    class_: str
    url_path: str
    name: str
    updated_on: int
    color: str
    lighter_text_color: str
    darker_text_color: str
    is_default: bool
    position: int
    project_id: int | None

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def project_label_from_json(json_obj: dict) -> AcProjectLabel:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_PROJECT_LABEL
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    return AcProjectLabel(**json_obj)
