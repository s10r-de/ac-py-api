import dataclasses
import json
from dataclasses import dataclass

from ActiveCollabAPI import AC_CLASS_TASK_LABEL, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


@dataclass
class AcTaskLabel:
    color: str
    darker_text_color: str
    id: int
    lighter_text_color: str
    name: str
    is_default: bool = dataclasses.field(default=False)
    is_global: bool = dataclasses.field(default=False)
    position: int = dataclasses.field(default=0)
    project_id: int | None = dataclasses.field(default=None)
    updated_on: int | None = dataclasses.field(default=None)
    url_path: str = dataclasses.field(default="")
    class_: str = dataclasses.field(default=AC_CLASS_TASK_LABEL)

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


def task_label_from_task_json(json_obj: dict) -> AcTaskLabel:
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    return AcTaskLabel(**json_obj)
