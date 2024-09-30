import dataclasses
import json
from dataclasses import dataclass


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
        d["class"] = d["class_"]
        del d["class_"]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def project_label_from_json(json_obj: dict) -> AcProjectLabel:
    assert json_obj["class"] == "ProjectLabel"
    json_obj["class_"] = json_obj["class"]
    del json_obj["class"]
    return AcProjectLabel(**json_obj)
