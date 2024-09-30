import dataclasses
import json
from dataclasses import dataclass


@dataclass
class AcProjectCategory:
    class_: str
    created_by_email: str
    created_by_id: int
    created_by_name: str
    created_on: int
    id: int
    name: str
    parent_id: int | None
    parent_type: str | None
    updated_on: int
    url_path: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d["class"] = d["class_"]
        del d["class_"]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def project_category_from_json(json_obj: dict) -> AcProjectCategory:
    assert json_obj["class"] == "ProjectCategory"
    json_obj["class_"] = json_obj["class"]
    del json_obj["class"]
    return AcProjectCategory(**json_obj)
