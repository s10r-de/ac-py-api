from dataclasses import dataclass


@dataclass
class AcFileAccessToken:
    download_token: str
    preview_token: str
    thumb_token: str
    ttl: int


def fileaccesstoken_from_json(json_obj: dict) -> AcFileAccessToken:
    return AcFileAccessToken(**json_obj)
