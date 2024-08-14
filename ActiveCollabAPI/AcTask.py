import dataclasses
import json
from dataclasses import dataclass

from ActiveCollabAPI import AcTaskDependencies


@dataclass
class AcTask:
    assignee_id: int
    attachments: []
    body: str
    body_formatted: str
    body_mode: str
    class_: str
    comments_count: int
    completed_by_id: int
    completed_on: int
    completed_subtasks: int
    created_by_email: str
    created_by_id: int
    created_by_name: str
    created_from_recurring_task_id: int
    created_on: int
    delegated_by_id: int
    due_on: int
    estimate: int
    fake_assignee_email: str
    fake_assignee_name: str
    id: int
    is_billable: bool
    is_completed: bool
    is_hidden_from_clients: bool
    is_important: bool
    is_trashed: bool
    job_type_id: int
    labels: []
    name: str
    open_dependencies: AcTaskDependencies
    open_subtasks: int
    position: int
    project_id: int
    start_on: int
    task_list_id: int
    task_number: int
    total_subtasks: int
    trashed_by_id: int
    trashed_on: int
    updated_by_id: int
    updated_on: int
    url_path: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d["class"] = d["class_"]
        del d["class_"]
        if d["open_dependencies"] is not None:
            d["open_dependencies"] = self.open_dependencies.to_dict()
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def task_from_json(json_obj: dict) -> AcTask:
    json_obj["class_"] = json_obj["class"]
    del json_obj["class"]
    if json_obj["open_dependencies"] is not None:
        json_obj["open_dependencies"] = AcTaskDependencies.taskdependency_from_json(json_obj["open_dependencies"])
    return AcTask(**json_obj)
