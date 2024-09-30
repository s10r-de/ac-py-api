import dataclasses
import json
from dataclasses import dataclass


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
        d["class"] = d["class_"]
        del d["class_"]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def task_label_from_json(json_obj: dict) -> AcTaskLabel:
    assert json_obj["class"] == "TaskLabel"
    json_obj["class_"] = json_obj["class"]
    del json_obj["class"]
    return AcTaskLabel(**json_obj)
