import dataclasses
import json
from dataclasses import dataclass

from ActiveCollabAPI import AC_CLASS_TASK_LABEL, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


@dataclass
class AcTaskLabel:
    class_: str
    color: str
    darker_text_color: str
    id: int
    is_default: bool
    is_global: bool
    lighter_text_color: str
    name: str
    position: int
    project_id: int | None
    updated_on: int
    url_path: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def task_label_from_json(json_obj: dict) -> AcTaskLabel:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_TASK_LABEL
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    return AcTaskLabel(**json_obj)
