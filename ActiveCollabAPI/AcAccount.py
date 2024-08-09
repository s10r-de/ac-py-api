import dataclasses
import json
from dataclasses import dataclass


@dataclass
class AcAccount:
    name: int
    url: str
    display_name: str
    user_display_name: str
    position: int
    class_: str
    status: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d["class"] = d["class_"]
        del d["class_"]
        return d

    def to_json(self) -> json:
        return json.dumps(self.to_dict())


def account_from_json(a) -> AcAccount:
    a["class_"] = a["class"]
    del a["class"]
    return AcAccount(**a)
