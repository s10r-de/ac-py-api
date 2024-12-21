import dataclasses
import json
import logging
from dataclasses import dataclass

from active_collab_api import (
    AC_CLASS_COMPANY,
    AC_ERROR_WRONG_CLASS,
    AC_PROPERTY_CLASS,
    AC_PROPERTY_CLASS_,
)
from active_collab_api.ac_data_object import AcDataObject


@dataclass
class AcCompany(AcDataObject):
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
    members: list[int]
    name: str
    phone: str | None
    trashed_by_id: int
    trashed_on: int | None
    updated_by_id: int
    updated_on: int
    url_path: str
    tax_id: str | None = dataclasses.field(default=None)
    tax_number: str | None = dataclasses.field(default=None)
    default_invoice_due_after: int | None = dataclasses.field(default=None)
    default_invoice_recipients: str | None = dataclasses.field(default=None)
    address_line_1: str | None = dataclasses.field(default=None)
    address_line_2: str | None = dataclasses.field(default=None)
    city: str | None = dataclasses.field(default=None)
    zip_code: str | None = dataclasses.field(default=None)
    region: str | None = dataclasses.field(default=None)
    country: str | None = dataclasses.field(default=None)
    archived_on: int = dataclasses.field(default=0)

    def __eq__(self, other) -> bool:
        ignored_fields = ["members"]
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
                    "AcCompany[%d]: %s '%s'!='%s' - does not match -> FAIL"
                    % (self.id, key, this_value, other_value)
                )
                result = False
            else:
                logging.debug(
                    "AcCompany[%d]: %s '%s' - matches -> OK"
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


def company_from_json(json_obj: dict) -> AcCompany:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_COMPANY, (
        AC_ERROR_WRONG_CLASS + " " + json_obj[AC_PROPERTY_CLASS]
    )
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    return AcCompany(**json_obj)
