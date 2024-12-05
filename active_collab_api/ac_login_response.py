from dataclasses import dataclass


@dataclass
class AcLoginResponse:
    is_ok: bool
    token: str
