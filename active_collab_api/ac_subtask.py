import dataclasses
import json
from dataclasses import dataclass

from active_collab_api import AC_CLASS_SUBTASK, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


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
    completed_by_name: str | None = dataclasses.field(default="")
    completed_by_email: str | None = dataclasses.field(default="")
    type: str | None = dataclasses.field(default=None)
    body: str = dataclasses.field(default="")

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def subtask_from_json(json_obj: dict) -> AcSubtask:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_SUBTASK
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    return AcSubtask(**json_obj)


def subtask_map_name_to_text(subtask: AcSubtask) -> AcSubtask:
    subtask.body = subtask.name
    return subtask
