from dataclasses import dataclass

from active_collab_api.AcAccount import AcAccount
from active_collab_api.AcLoginUser import AcLoginUser


@dataclass
class AcCloudLoginResponse:
    user: AcLoginUser
    accounts: list[AcAccount]
