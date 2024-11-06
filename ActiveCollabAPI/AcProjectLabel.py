import dataclasses
import json
import logging
from dataclasses import dataclass

from ActiveCollabAPI import AC_CLASS_PROJECT_LABEL, AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


@dataclass
class AcProjectLabel:
    id: int
    class_: str
    url_path: str
    name: str
    updated_on: int
    color: str
    lighter_text_color: str
    darker_text_color: str
    is_default: bool
    position: int
    project_id: int | None
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
                    "AcProjectLabel[%d]: %s '%s'!='%s' - does not match -> FAIL" % (
                        self.id, key, this_value, other_value))
                result = False
            else:
                logging.debug("AcProjectLabel[%d]: %s '%s' - matches -> OK" % (self.id, key, this_value))
        return result

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def project_label_from_json(json_obj: dict) -> AcProjectLabel:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_PROJECT_LABEL
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    return AcProjectLabel(**json_obj)
