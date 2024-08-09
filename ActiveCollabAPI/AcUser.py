import dataclasses
import json
from dataclasses import dataclass


@dataclass
class AcUser:
    avatar_url: str
    first_name: str
    last_name: str
    intent: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
