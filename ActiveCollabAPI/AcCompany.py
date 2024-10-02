import dataclasses
import json
from dataclasses import dataclass

from ActiveCollabAPI import AC_CLASS_COMPANY, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


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
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def company_from_json(json_obj: dict) -> AcCompany:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_COMPANY
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    return AcCompany(**json_obj)
