import argparse
import configparser
import http.client as http_client
import json
import logging
import os
import sys
import time
from collections.abc import Iterator

from active_collab_api import AC_CLASS_USER_MEMBER, AC_CLASS_USER_OWNER, AC_CLASS_TASK
from active_collab_api.ac_project import AcProject
from active_collab_api.ac_subtask import AcSubtask
from active_collab_api.ac_task import AcTask
from active_collab_api.ac_task_list import AcTaskList
from active_collab_api.ac_user import AcUser
from active_collab_api.active_collab import AcApiError, ActiveCollab
from active_collab_storage.storage import AcFileStorage

from active_collab_app.statistics import Statistics
from active_collab_app.version import VERSION
from active_collab_app.helper import map_user_id

overall_statistics = Statistics()


class DoNotDeleteCloud(Exception):
    pass


def setup_logging(log_level=logging.ERROR, http_debugging=False):
    root = logging.getLogger()
    root.setLevel(log_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)
    if http_debugging:
        # These two lines enable debugging at httplib level (requests->urllib3->http.client)
        http_client.HTTPConnection.debuglevel = 1


def load_config(args):
    if not os.path.exists(args.config):
        raise FileNotFoundError(f"Configfile '{args.config}' not found!")
    config = configparser.ConfigParser(interpolation=None)
    config.read(args.config)
    return config


def map_company_id(config: configparser.ConfigParser, from_company_id: int) -> int:
    option_name = f"map_company_id_{from_company_id}"
    if config.has_option("DEFAULLT", option_name):
        return config.getint("DEFAULT", option_name)
    return from_company_id


def serialize_output(output):
    # serialize the output
    return json.dumps(output, indent=4)


def run_testing(ac: ActiveCollab, config: configparser.ConfigParser):  # pylint: disable=unused-argument
    # account_id = config.getint("LOGIN", "account")
    # storage_path = config.get("STORAGE", "path")
    # ac_storage = AcFileStorage(storage_path, account_id)

    result = []

    # https://ac-backup.[example].de/projects/745?modal=Task-37180-745
    project_id = 745
    task_id = 37180
    task_number = 1629

    task = AcTask(project_id=project_id,
                  id=task_id,
                  task_number=task_number,
                  assignee_id=0,
                  attachments=[],
                  body="",
                  body_formatted="",
                  body_mode=None,
                  class_=AC_CLASS_TASK,
                  comments_count=0,
                  completed_by_id=0,
                  completed_on=0,
                  completed_subtasks=0,
                  created_by_email="",
                  created_by_id=0,
                  created_by_name="",
                  created_from_recurring_task_id=None,
                  created_on=0,
                  delegated_by_id=0,
                  due_on=0,
                  estimate=0,
                  fake_assignee_email="",
                  fake_assignee_name="",
                  is_billable=False,
                  is_completed=False,
                  is_hidden_from_clients=False,
                  is_important=False,
                  is_trashed=False,
                  job_type_id=0,
                  labels=[],
                  name="",
                  open_dependencies=None,
                  open_subtasks=None,
                  position=0,
                  start_on=0,
                  task_list_id=0,
                  total_subtasks=0,
                  trashed_by_id=0,
                  trashed_on=0,
                  updated_by_id=0,
                  updated_on=0,
                  url_path="")
    result = ac.update_task_set_task_number(task)

    return result
    # return map(lambda r: r.to_dict(), result)


def run_version():
    return {"version": VERSION}


def run_info(ac: ActiveCollab, config: configparser.ConfigParser):
    info = ac.get_info()
    info["is_cloud"] = check_is_cloud(config)
    return info


def run_dump_all(ac: ActiveCollab, config: configparser.ConfigParser):
    account_id = config.getint("LOGIN", "account")
    storage_path = config.get("STORAGE", "path")

    ac_storage = AcFileStorage(storage_path, account_id)
    ac_storage.reset()
    ac_storage.ensure_dirs()

    dump_all_companies(ac, ac_storage)
    dump_all_users(ac, ac_storage)
    dump_all_project_categories(ac, ac_storage)
    dump_all_project_labels(ac, ac_storage)
    dump_all_task_labels(ac, ac_storage)
    dump_all_projects_with_all_data(ac, ac_storage)

    return {
        "account": account_id,
        "storage_path": storage_path,
        "statistics": overall_statistics.get(),
    }


def dump_all_projects_with_all_data(ac, ac_storage):
    for project in ac.get_all_projects():
        ac_storage.data_objects["projects"].save(project)
        dump_all_project_notes(ac, ac_storage, project)
        dump_all_task_lists_of_project(ac, ac_storage, project)
        dump_all_tasks_of_project(ac, ac_storage, project)


def dump_all_project_notes(ac, ac_storage, project):
    for project_note in ac.get_project_notes(project):
        ac_storage.data_objects["project-notes"].save(project_note)
        overall_statistics.project_notes.increment()
        for attachment in project_note.attachments:
            dump_attachment(ac, ac_storage, attachment)


def dump_all_task_lists_of_project(ac, ac_storage, project):
    for task_list in ac.get_project_all_task_lists(project):
        ac_storage.data_objects["task-lists"].save(task_list)
        overall_statistics.task_lists.increment()


def dump_all_tasks_of_project(ac, ac_storage, project):
    for task in ac.get_all_tasks(project.id):
        ac_storage.data_objects["tasks"].save(task)
        overall_statistics.tasks.increment()
        for attachment in task.get_attachments():
            dump_attachment(ac, ac_storage, attachment)
        if task.total_subtasks > 0:
            dump_task_subtasks(ac, ac_storage, task)
        if task.comments_count > 0:
            dump_task_comments(ac, ac_storage, task)
        dump_task_history(ac, ac_storage, task)


def dump_attachment(ac, ac_storage, attachment):
    ac_storage.data_objects["attachments"].save(
        attachment, ac.download_attachment(attachment)
    )
    overall_statistics.attachments.increment()


def dump_task_comments(ac, ac_storage, task):
    for comment in ac.get_comments(task):
        ac_storage.data_objects["comments"].save(comment)
        overall_statistics.task_comments.increment()
        for attachment in comment.get_attachments():
            dump_attachment(ac, ac_storage, attachment)


def dump_task_history(ac, ac_storage, task):
    for history in ac.get_task_history(task):
        ac_storage.data_objects["task-history"].save(history)
        overall_statistics.task_history.increment()


def dump_task_subtasks(ac, ac_storage, task):
    for subtask in ac.get_subtasks(task):
        ac_storage.data_objects["subtasks"].save(subtask)
        overall_statistics.subtasks.increment()


def dump_all_task_labels(ac, ac_storage):
    for task_label in ac.get_task_labels():
        ac_storage.data_objects["task-labels"].save(task_label)
        overall_statistics.task_labels.increment()


def dump_all_project_labels(ac, ac_storage):
    for project_label in ac.get_project_labels():
        ac_storage.data_objects["project-labels"].save(project_label)
        overall_statistics.project_labels.increment()


def dump_all_project_categories(ac, ac_storage):
    for project_category in ac.get_project_categories():
        ac_storage.data_objects["project-categories"].save(project_category)
        overall_statistics.project_categories.increment()


def dump_all_users(ac, ac_storage):
    for user in ac.get_all_users():
        ac_storage.data_objects["users"].save(user)
        overall_statistics.users.increment()


def dump_all_companies(ac, ac_storage):
    for company in ac.get_all_companies():
        ac_storage.data_objects["companies"].save(company)
        overall_statistics.companies.increment()


def _login(config: configparser.ConfigParser) -> ActiveCollab:
    # create the AC Client
    base_url = config.get("DEFAULT", "base_url")
    is_cloud = config.getboolean("DEFAULT", "is_cloud", fallback=False)
    account = ""
    if is_cloud:
        account = config.get("LOGIN", "account", fallback="")
    ac = ActiveCollab(base_url, is_cloud)
    ac.login(config.get("LOGIN", "username"), config.get("LOGIN", "password"), account)
    return ac


def check_is_cloud(config: configparser.ConfigParser) -> bool:
    is_cloud = config.getboolean("DEFAULT", "is_cloud", fallback=False)
    if is_cloud is False:
        base_url = config.get("DEFAULT", "base_url")
        if base_url.startswith("https://activecollab.com"):
            is_cloud = True
    return is_cloud


def run_delete_all(ac: ActiveCollab, config: configparser.ConfigParser):
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


def run_empty_trash(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not empty trash from cloud!")
    return ac.empty_trash()  # FIXME loop until empty


def run_verify_all(ac: ActiveCollab, config: configparser.ConfigParser):
    account_id = config.getint("LOGIN", "account")
    storage_path = config.get("STORAGE", "path")
    ac_storage = AcFileStorage(storage_path, account_id)
    logging.info("Be sure to empty cache in filesystem before testing!")
    logging.info("  rm -fr var/www/html/cache/*")
    _verify_companies(ac, ac_storage)
    _verify_users(ac, ac_storage)
    _verify_project_categories(ac, ac_storage)
    _verify_project_labels(ac, ac_storage)
    _verify_projects(ac, ac_storage)
    _verify_task_lists(ac, ac_storage)
    _verify_tasks(ac, ac_storage)
    # _verify_comments(ac, ac_storage)


def _verify_project_labels(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
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


def _verify_project_categories(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
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


def _verify_tasks(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
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


def _verify_task_lists(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    result = True
    for task_list_id in ac_storage.data_objects["task-lists"].list_ids():
        task_list = ac_storage.data_objects["task-lists"].load(task_list_id)
        project_id = task_list.project_id
        server_all_project_task_lists = []
        try:
            server_all_project_task_lists = ac.get_project_task_lists(project_id)
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


def _verify_projects(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    result = True
    server_projects = ac.get_all_projects()
    for project_id in ac_storage.data_objects["projects"].list_ids():
        company = ac_storage.data_objects["projects"].load(project_id)
        server_project = list(
            filter(lambda c, pj_id=project_id: c.id == pj_id, server_projects)
        )
        if len(server_project) == 0:
            logging.error("Project %d not found!" % project_id)
            result = False
            continue
        if company != server_project[0]:
            logging.error("Project %d does not match!" % project_id)
            result = False
            continue
    return result


def _verify_companies(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
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


def _verify_users(ac: ActiveCollab, ac_storage: AcFileStorage):
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


def run_load_all(ac: ActiveCollab, config: configparser.ConfigParser):
    account_id = config.getint("LOGIN", "account")
    storage_path = config.get("STORAGE", "path")
    ac_storage = AcFileStorage(storage_path, account_id)

    _load_companies(ac, ac_storage)  # TODO: archived companies
    archived_users = _load_users(config, ac, ac_storage)

    _load_project_categories(ac, ac_storage)  # TODO: archived categories
    _load_project_labels(ac, ac_storage)  # TODO: archived labels

    complete_projects = _load_projects(config, ac, ac_storage)
    complete_task_lists = _load_task_lists(ac, ac_storage)
    complete_tasks = _load_tasks(ac, ac_storage)
    complete_subtasks = _load_subtasks(ac, ac_storage)

    _load_comments(ac, ac_storage)  # TODO: archived comments?
    _load_attachments(ac, ac_storage)  # TODO: archived attachments?

    for subtask in complete_subtasks:
        ac.complete_subtask(subtask)
    for task in complete_tasks:
        ac.complete_task(task)
    for task_list in complete_task_lists:
        ac.complete_task_list(task_list)
    for project in complete_projects:
        ac.complete_project(project)
    for user in archived_users:
        ac.archive_user(user)


def _delete_all_tasks(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    for project in ac.get_all_projects():
        ac.delete_all_tasks(project.id)


def _delete_all_task_lists(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    for project in ac.get_all_projects():
        ac.delete_all_task_lists(project)


def _delete_all_projects(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    return ac.delete_all_projects()


def _delete_all_project_categories(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    return ac.delete_all_project_categories()


def _delete_all_project_labels(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    return ac.delete_all_project_labels()


def _delete_all_users(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    return ac.delete_all_users()


def _delete_all_companies(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise DoNotDeleteCloud("Do not delete data from cloud!")
    return ac.delete_all_companies()


def _load_attachments(ac: ActiveCollab, ac_storage: AcFileStorage) -> int:
    cnt = 0
    for attachment_id in ac_storage.data_objects["attachments"].list_ids():
        attachment = ac_storage.data_objects["attachments"].load(attachment_id)
        bin_file = ac_storage.data_objects["attachments"].get_bin_filename(attachment)
        logging.debug("Uploading file %s" % bin_file)
        if ac.upload_attachment(attachment, bin_file):
            cnt += 1
    return cnt


def _load_comments(ac: ActiveCollab, ac_storage: AcFileStorage) -> int:
    cnt = 0
    for comment_id in ac_storage.data_objects["comments"].list_ids():
        comment = ac_storage.data_objects["comments"].load(comment_id)
        if ac.create_comment(comment):
            cnt += 1
    return cnt


def _load_subtasks(ac: ActiveCollab, ac_storage: AcFileStorage) -> list[AcSubtask]:
    completed = []
    for subtask_id in ac_storage.data_objects["subtasks"].list_ids():
        subtask = ac_storage.data_objects["subtasks"].load(subtask_id)
        if subtask.is_completed:
            completed.append(subtask)
            subtask.is_completed = False
            subtask.completed_by_id = None
            subtask.completed_on = None
        ac.create_subtask(subtask)
    return completed


def _load_tasks(ac: ActiveCollab, ac_storage: AcFileStorage) -> list[AcTask]:
    completed = []
    for task_id in ac_storage.data_objects["tasks"].list_ids():
        task = ac_storage.data_objects["tasks"].load(task_id)
        if task.is_completed:
            completed.append(task)
            task.is_completed = False
            task.completed_by_id = None
            task.completed_on = None
        ac.create_task(task)
    _fix_task_number(ac, ac_storage, 10000)
    _fix_task_number(ac, ac_storage)
    return completed


def _fix_task_number(ac: ActiveCollab, ac_storage: AcFileStorage, offset: int = 0) -> None:
    tasks = ac_storage.data_objects["tasks"].list_ids()
    if tasks is None:
        return
    tasks.reverse()
    for task_id in tasks:
        task = ac_storage.data_objects["tasks"].load(task_id)
        task.task_number = task.task_number + offset
        ac.update_task_set_task_number(task)


def _load_task_lists(ac: ActiveCollab, ac_storage: AcFileStorage) -> list[AcTaskList]:
    completed = []
    for task_list_id in ac_storage.data_objects["task-lists"].list_ids():
        task_list = ac_storage.data_objects["task-lists"].load(task_list_id)
        if task_list.is_completed:
            completed.append(task_list)
            task_list.is_completed = False
            task_list.completed_by_id = None
            task_list.completed_on = None
            task_list.open_tasks = 0
        ac.create_task_list(task_list)
    return completed


def _load_projects(
    config: configparser.ConfigParser, ac: ActiveCollab, ac_storage: AcFileStorage
) -> list[AcProject]:
    completed = []
    for project_id in ac_storage.data_objects["projects"].list_ids():
        project = ac_storage.data_objects["projects"].load(project_id)
        project.company_id = map_company_id(config, project.company_id)
        project.members = map(lambda uid, cfg=config: map_user_id(cfg, uid), project.members)
        if project.is_completed:
            completed.append(project)
            project.is_completed = False
            project.completed_on = None
            project.completed_by_id = None
        ac.create_project(project)
    _fix_project_number(ac, ac_storage, 10000)
    _fix_project_number(ac, ac_storage)
    return completed


def _fix_project_number(ac: ActiveCollab, ac_storage: AcFileStorage, offset: int = 0) -> None:
    projects = ac_storage.data_objects["projects"].list_ids()
    if projects is None:
        return
    projects.reverse()
    for project_id in projects:
        project = ac_storage.data_objects["projects"].load(project_id)
        project.project_number = project.project_number + offset
        ac.update_project_set_project_number(project)


def _load_project_labels(ac: ActiveCollab, ac_storage: AcFileStorage) -> int:
    cnt = 0
    for project_label_id in ac_storage.data_objects["project-labels"].list_ids():
        project_label = ac_storage.data_objects["project-labels"].load(project_label_id)
        if ac.create_project_label(project_label):
            cnt += 1
    return cnt


def _load_project_categories(ac: ActiveCollab, ac_storage: AcFileStorage) -> int:
    cnt = 0
    for project_category_id in ac_storage.data_objects["project-categories"].list_ids():
        project_category = ac_storage.data_objects["project-categories"].load(
            project_category_id
        )
        if ac.create_project_category(project_category):
            cnt += 1
    return cnt


def _load_users(
    config: configparser.ConfigParser, ac: ActiveCollab, ac_storage: AcFileStorage
) -> list[AcUser]:
    archived = []
    for user_id in ac_storage.data_objects["users"].list_ids():
        user = ac_storage.data_objects["users"].load(user_id)
        user.company_id = map_company_id(config, user.company_id)
        if user.is_archived:
            archived.append(user)
            user.is_archived = False
        if user.class_ == AC_CLASS_USER_OWNER:
            user.class_ = AC_CLASS_USER_MEMBER
        ac.create_user(user)
    return archived


def _load_companies(ac: ActiveCollab, ac_storage: AcFileStorage) -> int:
    cnt = 0
    for company_id in ac_storage.data_objects["companies"].list_ids():
        company = ac_storage.data_objects["companies"].load(company_id)
        if ac.create_company(company):
            cnt += 1
    return cnt


def run(args, parser, config: configparser.ConfigParser):  # pylint: disable=R0911
    # run the commands
    if args.command == "version":
        return run_version()
    if args.command == "info":
        return run_info(_login(config), config)
    if args.command == "dump":
        return run_dump_all(_login(config), config)
    if args.command == "delete":
        return run_delete_all(_login(config), config)
    if args.command == "empty":
        return run_empty_trash(_login(config), config)
    if args.command == "verify":
        return run_verify_all(_login(config), config)
    if args.command == "load":
        return run_load_all(_login(config), config)
    if args.command == "testing":
        return run_testing(_login(config), config)

    # no command given so show the help
    parser.print_help()
    return None


def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        prog="acdump",
        description="This is a tool to dump data from Active-Collab",
        epilog="(c) 2024 by ACME VC, Charlie Sloan <cs@example.com>",
    )
    parser.add_argument(
        "-c", "--config", required=True, help="use the named config file"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable some move verbose output"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument(
        "--http-debug", action="store_true", help="Enable HTTP debug output"
    )
    parser.add_argument(
        "command",
        choices=[
            "version",
            "info",
            "dump",
            "delete",
            "empty",
            "verify",
            "load",
            "testing",
        ],
        help="The command to run",
    )
    args = parser.parse_args()
    config = load_config(args)
    log_level = logging.ERROR
    if args.verbose:
        log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG
    setup_logging(log_level, args.http_debug)
    t_start = time.time()
    logging.info("Started")
    output = run(args, parser, config)
    if isinstance(output, Iterator):
        output = list(output)
    if output is not None:
        print(serialize_output(output))
    logging.info("Finished after %0.3f seconds" % (time.time() - t_start))


if __name__ == "__main__":
    main()
