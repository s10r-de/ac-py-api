import dataclasses
import json
from dataclasses import dataclass


@dataclass
class AcCompany:
    address: str | None
    class_: str
    created_by_email: str | None
    created_by_id: int
    created_by_name: str | None
    created_on: int
    currency_id: int
    has_note: bool
    homepage_url: str
    id: int
    is_archived: bool
    is_owner: bool
    is_trashed: bool
    members: [int]
    name: str
    phone: str | None
    tax_id: str | None
    trashed_by_id: int
    trashed_on: int | None
    updated_by_id: int
    updated_on: int
    url_path: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def company_from_json(json_obj: dict) -> AcCompany:
    assert json_obj["class"] == "Company"
    json_obj["class_"] = json_obj["class"]
    del json_obj["class"]
    return AcCompany(**json_obj)
