from dataclasses import dataclass

from ActiveCollabAPI.AcUser import AcUser
from ActiveCollabAPI.AcAccount import AcAccount


@dataclass
class AcLoginResponse:
    user: AcUser
    accounts: list[AcAccount]
