import dataclasses
import json
from dataclasses import dataclass

from ActiveCollabAPI import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_, AC_ERROR_WRONG_CLASS, AC_CLASS_ACCOUNT


@dataclass
class AcAccount:
    name: int
    url: str
    display_name: str
    user_display_name: str
    position: int
    class_: str
    status: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> json:
        return json.dumps(self.to_dict())


def account_from_json(a) -> AcAccount:
    assert a[AC_PROPERTY_CLASS] == AC_CLASS_ACCOUNT, AC_ERROR_WRONG_CLASS
    a[AC_PROPERTY_CLASS_] = a[AC_PROPERTY_CLASS]
    del a[AC_PROPERTY_CLASS]
    return AcAccount(**a)
