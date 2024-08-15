import dataclasses
import json
from dataclasses import dataclass


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

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d["class"] = d["class_"]
        del d["class_"]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def project_from_json(json_obj: dict) -> AcProject:
    json_obj["class_"] = json_obj["class"]
    del json_obj["class"]
    return AcProject(**json_obj)
