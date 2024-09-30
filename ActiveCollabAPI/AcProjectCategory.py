import dataclasses
import json
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
