import dataclasses
import json
from dataclasses import dataclass

from active_collab_api.ac_account import AcAccount
from active_collab_api.ac_login_user import AcLoginUser
from active_collab_api.ac_token import AcToken


@dataclass
class AcSession:
    user: AcLoginUser
    accounts: list[AcAccount]
    cur_account: AcAccount
    token: AcToken

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d["accounts"] = list(map(lambda a: a.to_dict(), self.accounts))
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
