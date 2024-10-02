import dataclasses
import json
from dataclasses import dataclass

from AcAttachment import AcAttachment, attachment_from_json
from AcTaskDependencies import taskdependency_from_json
from ActiveCollabAPI import AcTaskDependencies, AC_CLASS_TASK, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


@dataclass
class AcTask:
    assignee_id: int
    attachments: [AcAttachment | None]
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
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        if d["open_dependencies"] is not None:
            d["open_dependencies"] = self.open_dependencies.to_dict()
        if d["attachments"] is not None:
            d["attachments"] = list(map(lambda a: a.to_dict(), self.get_attachments()))
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def get_attachments(self) -> list[AcAttachment]:
        return self.attachments


def task_from_json(json_obj: dict) -> AcTask:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_TASK
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    if json_obj["open_dependencies"] is not None:
        json_obj["open_dependencies"] = taskdependency_from_json(json_obj["open_dependencies"])
    if json_obj["attachments"] is not None:
        json_obj["attachments"] = list(map(attachment_from_json, json_obj["attachments"]))
    return AcTask(**json_obj)
