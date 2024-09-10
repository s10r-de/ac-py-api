import dataclasses
import json
from dataclasses import dataclass

from ActiveCollabAPI.AcAccount import AcAccount
from ActiveCollabAPI.AcToken import AcToken
from ActiveCollabAPI.AcLoginUser import AcLoginUser


@dataclass
class AcSession:
    user: AcLoginUser
    accounts: [AcAccount]
    cur_account: AcAccount
    token: AcToken

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d["accounts"] = list(map(lambda a: a.to_dict(), self.accounts))
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
