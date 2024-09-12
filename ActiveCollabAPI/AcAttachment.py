import dataclasses
import json
from dataclasses import dataclass


@dataclass
class AcAttachment:
    id: int
    class_: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d["class"] = d["class_"]
        del d["class_"]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def attachment_from_json(json_obj: dict) -> AcAttachment:
    json_obj["class_"] = json_obj["class"]
    del json_obj["class"]
    return AcAttachment(**json_obj)
