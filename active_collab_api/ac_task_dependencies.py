import dataclasses
import json
from dataclasses import dataclass


@dataclass
class AcTaskDependencies:
    parents_count: int
    children_count: int

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def taskdependency_from_json(json_obj: dict) -> AcTaskDependencies:
    return AcTaskDependencies(**json_obj)
