import dataclasses
import json
from dataclasses import dataclass


@dataclass
class AcUser:
    additional_email_addresses: []
    avatar_url: str
    avatar_version: str
    class_: str
    company_id: int
    created_by_email: str
    created_by_id: int
    created_by_name: str
    created_on: int
    custom_permissions: []
    daily_capacity: int | None
    display_name: str
    email: str
    first_login_on: int
    first_name: str
    has_custom_avatar: bool
    id: int
    im_handle: str | None
    im_type: str | None
    is_archived: bool
    is_authenticator_validated: bool
    is_email_at_example: bool
    is_pending_activation: bool
    is_trashed: bool
    language_id: int
    last_name: str
    phone: str | None
    short_display_name: str
    title: str | None
    trashed_by_id: int
    trashed_on: int
    updated_on: int
    url_path: str
    workspace_count: int

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def user_from_json(json_obj: dict) -> AcUser:
    assert json_obj["class"] == "Member" or json_obj["class"] == "Owner"
    json_obj["class_"] = json_obj["class"]
    del json_obj["class"]
    return AcUser(**json_obj)
