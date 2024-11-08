import dataclasses
import json
from dataclasses import dataclass

from ActiveCollabAPI import (
    AC_PROPERTY_CLASS,
    AC_PROPERTY_CLASS_,
    AC_ERROR_WRONG_CLASS, AC_CLASS_ATTACHMENT_UPLOAD_RESPONSE,
)


@dataclass
class AcAttachmentUploadResponse:
    class_: str
    code: str
    name: str
    mime_type: str
    size: int
    thumbnail_url: str

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d[AC_PROPERTY_CLASS] = d[AC_PROPERTY_CLASS_]
        del d[AC_PROPERTY_CLASS_]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def attachment_upload_response_from_json(json_obj: dict) -> AcAttachmentUploadResponse:
    assert json_obj[AC_PROPERTY_CLASS] == AC_CLASS_ATTACHMENT_UPLOAD_RESPONSE, AC_ERROR_WRONG_CLASS + " " + json_obj[
        AC_PROPERTY_CLASS]
    json_obj[AC_PROPERTY_CLASS_] = json_obj[AC_PROPERTY_CLASS]
    del json_obj[AC_PROPERTY_CLASS]
    return AcAttachmentUploadResponse(**json_obj)
