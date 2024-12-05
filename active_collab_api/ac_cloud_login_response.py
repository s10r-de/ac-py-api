from dataclasses import dataclass

from active_collab_api.ac_account import AcAccount
from active_collab_api.ac_login_user import AcLoginUser


@dataclass
class AcCloudLoginResponse:
    user: AcLoginUser
    accounts: list[AcAccount]
