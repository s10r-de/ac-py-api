from dataclasses import dataclass

from ActiveCollabAPI.AcAccount import AcAccount
from ActiveCollabAPI.AcLoginUser import AcLoginUser


@dataclass
class AcCloudLoginResponse:
    user: AcLoginUser
    accounts: list[AcAccount]
