import configparser

from active_collab_api.ac_task import AcTask
from active_collab_api.active_collab import ActiveCollab


def run_testing(ac: ActiveCollab, config: configparser.ConfigParser):  # pylint: disable=unused-argument
    result = []

    # put your code for testing here

    # account_id = config.getint("LOGIN", "account")
    # storage_path = config.get("STORAGE", "path")
    # ac_storage = AcFileStorage(storage_path, account_id)

    project_id=23
    tasks = ac.get_all_tasks(project_id)

    result = list(map(AcTask.to_dict, tasks))

    return result
