from dataclasses import dataclass

from ActiveCollabAPI.AcLoginUser import AcLoginUser
from ActiveCollabAPI.AcAccount import AcAccount


@dataclass
class AcLoginResponse:
    user: AcLoginUser
    accounts: list[AcAccount]
