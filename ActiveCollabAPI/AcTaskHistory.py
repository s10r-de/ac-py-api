import dataclasses
import json
from dataclasses import dataclass


@dataclass
class AcTaskHistory:
    timestamp: int
    created_by_id: int
    created_by_name: str
    created_by_email: str
    modifications: []
    task_id: int = dataclasses.field(default=0)

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def task_history_from_json(json_obj: dict, task_id: int = 0) -> AcTaskHistory:
    json_obj["task_id"] = task_id
    return AcTaskHistory(**json_obj)
