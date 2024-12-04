import dataclasses
import json
import logging
from dataclasses import dataclass

from active_collab_api import AC_CLASS_TASK_LIST, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


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
                    "AcTaskList[%d]: %s '%s'!='%s' - does not match -> FAIL"
                    % (self.id, key, this_value, other_value)
                )
                result = False
            else:
                logging.debug(
                    "AcTaskList[%d]: %s ='%s' - matches -> OK"
                    % (self.id, key, this_value)
                )
        return result

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def task_list_from_json(json_obj: dict) -> AcTaskList:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_TASK_LIST
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    return AcTaskList(**json_obj)
