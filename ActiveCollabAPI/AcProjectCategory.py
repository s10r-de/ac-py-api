import dataclasses
import json
import logging
from dataclasses import dataclass

from ActiveCollabAPI import AC_CLASS_PROJECT_CATEGORY, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


@dataclass
class AcProjectCategory:
    class_: str
    created_by_email: str
    created_by_id: int
    created_by_name: str
    created_on: int
    id: int
    name: str
    parent_id: int | None
    parent_type: str | None
    updated_on: int
    url_path: str
    type: str | None = dataclasses.field(default=None)

    def __eq__(self, other) -> bool:
        ignored_fields = []
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
                    "AcProjectCategory[%d]: %s '%s'!='%s' - does not match -> FAIL" % (
                        self.id, key, this_value, other_value))
                result = False
            else:
                logging.debug(
                    "AcProjectCategory[%d]: %s '%s' - matches -> OK" % (self.id, key, this_value))
        return result

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def project_category_from_json(json_obj: dict) -> AcProjectCategory:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_PROJECT_CATEGORY
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    return AcProjectCategory(**json_obj)
