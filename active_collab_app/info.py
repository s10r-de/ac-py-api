import configparser

from active_collab_api.active_collab import ActiveCollab
from active_collab_app.helper import check_is_cloud


def run_info(ac: ActiveCollab, config: configparser.ConfigParser):
    info = ac.get_info()
    info["is_cloud"] = check_is_cloud(config)
    return info
