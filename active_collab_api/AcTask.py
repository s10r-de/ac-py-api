import dataclasses
import json
import logging
from dataclasses import dataclass

from active_collab_api.AcAttachment import AcAttachment, attachment_from_json
from active_collab_api.AcTaskDependencies import (
    AcTaskDependencies,
    taskdependency_from_json,
)
from active_collab_api.AcTaskLabel import AcTaskLabel, task_label_from_task_json
from active_collab_api import (
    AC_CLASS_TASK,
    AC_PROPERTY_CLASS,
    AC_PROPERTY_CLASS_,
    AC_ERROR_WRONG_CLASS,
)


@dataclass
class AcTask:
    assignee_id: int
    attachments: list[AcAttachment]
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
    labels: list[AcTaskLabel]
    name: str
    open_dependencies: AcTaskDependencies | None
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
    completed_by_name: str | None = dataclasses.field(default="")
    completed_by_email: str | None = dataclasses.field(default="")
    type: str | None = dataclasses.field(default=None)

    def __eq__(self, other) -> bool:
        ignored_fields = [
            "updated_on",
            "updated_by_id",
            "completed_on",
            "completed_by_id",
        ]
        result = True
        this_data = self.to_dict()
        other_data = other.to_dict()
        for key in this_data.keys():
            if key in ignored_fields:
                continue
            this_value = this_data[key]
            other_value = other_data[key]
            if this_value != other_value:
                logging.error(
                    "acTask[%d]: %s '%s'!='%s' - does not match -> FAIL"
                    % (self.id, key, this_value, other_value)
                )
                result = False
            else:
                logging.debug(
                    "acTask[%d]: %s '%s' - matches -> OK" % (self.id, key, this_value)
                )
        return result

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        if d["open_dependencies"] is not None:
            d["open_dependencies"] = self.open_dependencies.to_dict()
        if d["attachments"] is not None:
            d["attachments"] = list(map(lambda a: a.to_dict(), self.get_attachments()))
        if d["labels"] is not None:
            d["labels"] = list(map(lambda a: a.to_dict(), self.labels))
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def get_attachments(self) -> list[AcAttachment]:
        return self.attachments


def task_from_json(json_obj: dict) -> AcTask:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_TASK, AC_ERROR_WRONG_CLASS
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    if json_obj["open_dependencies"] is not None:
        json_obj["open_dependencies"] = taskdependency_from_json(
            json_obj["open_dependencies"]
        )
    if json_obj["attachments"] is not None:
        json_obj["attachments"] = list(
            map(attachment_from_json, json_obj["attachments"])
        )
    if json_obj["labels"] is not None:
        json_obj["labels"] = list(map(task_label_from_task_json, json_obj["labels"]))
    return AcTask(**json_obj)
