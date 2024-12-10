import configparser

from active_collab_api.active_collab import ActiveCollab
from active_collab_app.error import DoNotDeleteCloud
from active_collab_app.helper import check_is_cloud


def run_delete_all(ac: ActiveCollab, config: configparser.ConfigParser) -> bool:
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    # _delete_all_attachments(ac, config)
    _delete_all_task_lists(ac, config)
    _delete_all_tasks(ac, config)
    _delete_all_projects(ac, config)
    _delete_all_project_categories(ac, config)
    _delete_all_project_labels(ac, config)
    _delete_all_users(ac, config)
    _delete_all_companies(ac, config)
    return True


def _delete_all_tasks(ac: ActiveCollab, config: configparser.ConfigParser) -> None:
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    for project in ac.get_all_projects():
        ac.delete_all_tasks(project.id)


def _delete_all_task_lists(ac: ActiveCollab, config: configparser.ConfigParser) -> None:
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    for project in ac.get_all_projects():
        ac.delete_all_task_lists(project)


def _delete_all_projects(ac: ActiveCollab, config: configparser.ConfigParser) -> None:
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    return ac.delete_all_projects()


def _delete_all_project_categories(ac: ActiveCollab, config: configparser.ConfigParser) -> None:
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    return ac.delete_all_project_categories()


def _delete_all_project_labels(ac: ActiveCollab, config: configparser.ConfigParser) -> None:
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    return ac.delete_all_project_labels()


def _delete_all_users(ac: ActiveCollab, config: configparser.ConfigParser) -> None:
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    return ac.delete_all_users()


def _delete_all_companies(ac: ActiveCollab, config: configparser.ConfigParser) -> None:
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    return ac.delete_all_companies()
