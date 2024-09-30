import dataclasses
import json
from dataclasses import dataclass


@dataclass
class AcTaskList:
    class_: str
    completed_by_id: int | None
    completed_on: int | None
    completed_tasks: int
    created_by_email: str
    created_by_id: int
    created_by_name: str
    created_on: int
    due_on: int | None
    id: int
    is_completed: bool
    is_trashed: bool
    name: str
    open_tasks: int
    position: int
    project_id: int
    start_on: int | None
    trashed_by_id: int
    trashed_on: int | None
    updated_by_id: int
    updated_on: int
    url_path: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d["class"] = d["class_"]
        del d["class_"]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def task_list_from_json(json_obj: dict) -> AcTaskList:
    assert json_obj["class"] == "TaskList"
    json_obj["class_"] = json_obj["class"]
    del json_obj["class"]
    return AcTaskList(**json_obj)
