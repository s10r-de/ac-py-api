import dataclasses
import json
import logging
from dataclasses import dataclass

from ActiveCollabAPI import AC_CLASS_PROJECT, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


@dataclass
class AcProject:
    based_on_id: int | None
    based_on_type: str | None
    body: str
    body_formatted: str
    budget: float
    budget_type: str
    budgeting_interval: str
    category_id: int
    class_: str
    company_id: int
    completed_by_id: int | None
    completed_on: int | None
    count_discussions: int
    count_files: int
    count_notes: int
    count_tasks: int
    created_by_email: str
    created_by_id: int
    created_by_name: str
    created_on: int
    currency_id: int
    email: str
    file_size: int
    id: int
    is_billable: bool
    is_client_reporting_enabled: bool
    is_completed: bool
    is_estimate_visible_to_subcontractors: bool
    is_sample: bool
    is_tracking_enabled: bool
    is_trashed: bool
    label_id: int
    last_activity_on: int
    leader_id: int
    members: list[int]
    members_can_change_billable: bool
    name: str
    project_number: int
    show_task_estimates_to_clients: bool
    task_estimates_enabled: bool
    trashed_by_id: int
    trashed_on: bool
    updated_by_id: int | None
    updated_on: int | None
    url_path: str
    type: str | None = dataclasses.field(default=None)

    def __eq__(self, other) -> bool:
        result = True
        this_data = self.to_dict()
        other_data = other.to_dict()
        for key in this_data.keys():
            this_value = this_data[key]
            other_value = other_data[key]
            if this_value != other_value:
                logging.error(
                    "AcProject[%d]: %s '%s'!='%s' - does not match -> FAIL" % (self.id, key, this_value, other_value))
                result = False
            else:
                logging.debug(
                    "AcProject[%d]: %s ='%s' - matches -> OK" % (self.id, key, this_value))
        return result

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def project_from_json(json_obj: dict) -> AcProject:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_PROJECT
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    return AcProject(**json_obj)
