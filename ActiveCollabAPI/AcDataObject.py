import dataclasses
import json
from dataclasses import dataclass

from ActiveCollabAPI import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


@dataclass
class AcDataObject:

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        if hasattr(d, AC_PROPERTY_CLASS):
            d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
            del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
