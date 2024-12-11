import configparser
import logging

from active_collab_api.active_collab import ActiveCollab
from active_collab_api.ac_api_error import AcApiError
from active_collab_storage.storage import AcFileStorage


def run_verify_all(ac: ActiveCollab, config: configparser.ConfigParser) -> bool:
    result = False
    account_id = config.getint("LOGIN", "account")
    storage_path = config.get("STORAGE", "path")
    ac_storage = AcFileStorage(storage_path, account_id)
    logging.info("Be sure to empty cache in filesystem before testing!")
    logging.info("  rm -fr var/www/html/cache/*")
    result |= verify_companies(ac, ac_storage)
    result |= verify_users(ac, ac_storage)
    result |= verify_project_categories(ac, ac_storage)
    result |= verify_project_labels(ac, ac_storage)
    result |= verify_projects(ac, ac_storage)
    result |= verify_task_lists(ac, ac_storage)
    result |= verify_tasks(ac, ac_storage)
    # result |= _verify_comments(ac, ac_storage)
    return result


def verify_project_labels(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    result = True
    server_project_labels = ac.get_project_labels()
    for label_id in ac_storage.data_objects["project-labels"].list_ids():
        category = ac_storage.data_objects["project-labels"].load(label_id)
        server_labels = list(
            filter(
                lambda c, pj_label_id=label_id: c.id == pj_label_id,
                server_project_labels,
            )
        )
        if len(server_labels) == 0:
            logging.error("Project Label %d not found!" % label_id)
            result = False
            continue
        if category != server_labels[0]:
            logging.error("Project Label %d does not match!" % label_id)
            result = False
            continue
        logging.info("Project Label %d ok!" % label_id)
    return result


def verify_project_categories(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    result = True
    server_project_categories = ac.get_project_categories()
    for category_id in ac_storage.data_objects["project-categories"].list_ids():
        category = ac_storage.data_objects["project-categories"].load(category_id)
        server_category = list(
            filter(
                lambda c, cat_id=category_id: c.id == cat_id, server_project_categories
            )
        )
        if len(server_category) == 0:
            logging.error("Project Category %d not found!" % category_id)
            result = False
            continue
        if category != server_category[0]:
            logging.error("Project Category %d does not match!" % category_id)
            result = False
            continue
        logging.info("Project Category %d ok!" % category_id)
    return result


def verify_tasks(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    result = True
    # for each project
    all_server_tasks = []
    for server_project in ac.get_all_projects():
        all_server_tasks.extend(ac.get_all_tasks(server_project.id))
    # for all dumped tasks
    for task_id in ac_storage.data_objects["tasks"].list_ids():
        this_task = ac_storage.data_objects["tasks"].load(task_id)
        server_tasks = list(
            filter(lambda t, tt=this_task: tt.id == t.id, all_server_tasks)
        )
        if len(server_tasks) == 0:
            logging.error("Task %d not found!" % task_id)
            result = False
            continue
        if this_task != server_tasks[0]:
            logging.error("Task %d does not match!" % task_id)
            result = False
            continue

    return result

    # def _verify_comments(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    # result = True
    # load all comments from dump_task_history
    # if comment parentType = "Task"
    # get all comments from task from server
    # compare
    # return result


def verify_task_lists(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    result = True
    for task_list_id in ac_storage.data_objects["task-lists"].list_ids():
        task_list = ac_storage.data_objects["task-lists"].load(task_list_id)
        project_id = task_list.project_id
        server_all_project_task_lists = []
        try:
            server_all_project_task_lists = ac.get_project_all_task_lists_by_project_id(project_id)
        except AcApiError:
            pass  # ignore exception here
        if len(server_all_project_task_lists) == 0:
            logging.error("No task lists for project %d found!" % project_id)
            result = False
            continue
        server_task_list = list(
            filter(
                lambda o, tl_id=task_list.id: o.id == tl_id,
                server_all_project_task_lists,
            )
        )
        if len(server_task_list) == 0:
            logging.error(
                "Task list %d for project %d not found!" % (task_list.id, project_id)
            )
            result = False
            continue
        if task_list != server_task_list[0]:
            logging.error(
                "Task list %d for project %d does not match!"
                % (task_list.id, project_id)
            )
            result = False
    return result


def verify_projects(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    result = True
    server_projects = ac.get_all_projects()
    for project_id in ac_storage.data_objects["projects"].list_ids():
        project = ac_storage.data_objects["projects"].load(project_id)
        server_project = list(
            filter(lambda c, pj_id=project_id: c.id == pj_id, server_projects)
        )
        if len(server_project) == 0:
            logging.error("Project %d not found!" % project_id)
            result = False
            continue
        if project != server_project[0]:
            logging.error("Project %d does not match!" % project_id)
            result = False
            continue
    return result


def verify_companies(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    result = True
    server_companies = ac.get_all_companies()
    for company_id in ac_storage.data_objects["companies"].list_ids():
        company = ac_storage.data_objects["companies"].load(company_id)
        server_company = list(
            filter(lambda c, comp_id=company_id: c.id == comp_id, server_companies)
        )
        if len(server_company) == 0:
            logging.error("Company %d not found!" % company_id)
            result = False
            continue
        if company != server_company[0]:
            logging.error("Company %d does not match!" % company_id)
            result = False
            continue
        logging.info("Company %d ok!" % company_id)
    return result


def verify_users(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    result = True
    server_users = ac.get_all_users()
    for user_id in ac_storage.data_objects["users"].list_ids():
        company = ac_storage.data_objects["users"].load(user_id)
        server_user = list(filter(lambda c, uid=user_id: c.id == uid, server_users))
        if len(server_user) == 0:
            logging.error("User %d not found!" % user_id)
            result = False
            continue
        if company != server_user[0]:
            logging.error("User %d does not match!" % user_id)
            result = False
            continue
        logging.info("User %d ok!" % user_id)
    return result
