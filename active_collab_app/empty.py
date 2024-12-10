import configparser

from active_collab_api.active_collab import ActiveCollab
from active_collab_app.error import DoNotDeleteCloud
from active_collab_app.helper import check_is_cloud


def run_empty_trash(ac: ActiveCollab, config: configparser.ConfigParser) -> dict:
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not empty trash from cloud!")
    return ac.empty_trash()  # FIXME loop until empty
