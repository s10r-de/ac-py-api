import dataclasses
import json
from dataclasses import dataclass


@dataclass
class AcSubtask:
    assignee_id: int
    class_: str
    completed_by_id: int | None
    completed_on: int | None
    created_by_email: str
    created_by_id: int
    created_by_name: str
    created_on: int
    delegated_by_id: int
    due_on: int | None
    fake_assignee_email: str | None
    fake_assignee_name: str | None
    id: int
    is_completed: bool
    is_trashed: bool
    name: str
    position: int
    project_id: int
    task_id: int
    trashed_by_id: int
    trashed_on: int | None
    updated_on: int
    url_path: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d["class"] = d["class_"]
        del d["class_"]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def subtask_from_json(json_obj: dict) -> AcSubtask:
    json_obj["class_"] = json_obj["class"]
    del json_obj["class"]
    return AcSubtask(**json_obj)
