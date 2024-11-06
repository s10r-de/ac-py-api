import argparse
import configparser
import json
import logging
import os
import sys
from collections.abc import Iterator

from AcStorage.AcFileStorage import AcFileStorage
from ActiveCollabAPI.ActiveCollab import ActiveCollab


def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)


def load_config(args):
    if not os.path.exists(args.config):
        raise FileNotFoundError("Configfile '%s' not found!" % args.config)
    config = configparser.ConfigParser(interpolation=None)
    config.read(args.config)
    return config


def serialize_output(output):
    # serialize the output
    return json.dumps(output, indent=4)


def run_testing(ac, config: configparser.ConfigParser):
    account_id = config.getint("LOGIN", "account")
    storage_path = config.get("STORAGE", "path")
    ac_storage = AcFileStorage(storage_path, account_id)
    return ac_storage.data_objects["task-history"].list()


def run_version():
    from version import VERSION

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

    return {"message": "data of account %d dumped to %s" % (account_id, storage_path)}


def dump_all_projects_with_all_data(ac, ac_storage):
    projects = ac.get_active_projects()
    # projects.extend(ac.get_archived_projects()) # Task#64 ignore completed projects because not all related data is accessible over the API
    for project in projects:
        ac_storage.data_objects["projects"].save(project)
        dump_all_project_notes(ac, ac_storage, project)
        dump_all_task_lists_of_project(ac, ac_storage, project)
        dump_all_tasks_of_project(ac, ac_storage, project)


def dump_all_project_notes(ac, ac_storage, project):
    for project_note in ac.get_project_notes(project):
        ac_storage.data_objects["project-notes"].save(project_note)
        for attachment in project_note.attachments:
            dump_attachment(ac, ac_storage, attachment)


def dump_all_task_lists_of_project(ac, ac_storage, project):
    for task_list in ac.get_project_task_lists(project.id):
        ac_storage.data_objects["task-lists"].save(task_list)


def dump_all_tasks_of_project(ac, ac_storage, project):
    # tasks = ac.get_all_tasks(project.id)
    tasks = ac.get_active_tasks(project.id)
    for task in tasks:
        ac_storage.data_objects["tasks"].save(task)
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


def dump_task_comments(ac, ac_storage, task):
    for comment in ac.get_comments(task):
        ac_storage.data_objects["comments"].save(comment)
        for attachment in comment.get_attachments():
            dump_attachment(ac, ac_storage, attachment)


def dump_task_history(ac, ac_storage, task):
    for history in ac.get_task_history(task):
        ac_storage.data_objects["task-history"].save(history)


def dump_task_subtasks(ac, ac_storage, task):
    for subtask in ac.get_subtasks(task):
        ac_storage.data_objects["subtasks"].save(subtask)


def dump_all_task_labels(ac, ac_storage):
    for task_label in ac.get_task_labels():
        ac_storage.data_objects["task-labels"].save(task_label)


def dump_all_project_labels(ac, ac_storage):
    for project_label in ac.get_project_labels():
        ac_storage.data_objects["project-labels"].save(project_label)


def dump_all_project_categories(ac, ac_storage):
    for project_category in ac.get_project_categories():
        ac_storage.data_objects["project-categories"].save(project_category)


def dump_all_users(ac, ac_storage):
    for user in ac.get_all_users():
        ac_storage.data_objects["users"].save(user)


def dump_all_companies(ac, ac_storage):
    for company in ac.get_all_companies():
        ac_storage.data_objects["companies"].save(company)


def _login(config: configparser.ConfigParser) -> ActiveCollab:
    # create the AC Client
    base_url = config.get("DEFAULT", "base_url")
    is_cloud = config.getboolean("DEFAULT", "is_cloud", fallback=False)
    account = ""
    if is_cloud:
        account = config.get("LOGIN", "account", fallback=None)
    ac = ActiveCollab(base_url, is_cloud)
    ac.login(config.get("LOGIN", "username"),
             config.get("LOGIN", "password"), account)
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
        raise Exception("Do not delete data from cloud!")
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
        raise Exception("Do not empty trash from cloud!")
    return ac.empty_trash()  # FIXME loop until empty


def run_verify_all(ac: ActiveCollab, config: configparser.ConfigParser) -> int:
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
    _verify_comments(ac, ac_storage)


def _verify_project_labels(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    result = True
    server_project_labels = ac.get_project_labels()
    for label_id in ac_storage.data_objects["project-labels"].list_ids():
        category = ac_storage.data_objects["project-labels"].load(label_id)
        server_labels = list(
            filter(lambda c: c.id == label_id, server_project_labels))
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
        category = ac_storage.data_objects["project-categories"].load(
            category_id)
        server_category = list(
            filter(lambda c: c.id == category_id, server_project_categories)
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
        task = ac_storage.data_objects["tasks"].load(task_id)

        server_tasks = list(
            filter(lambda t: task.id == t.id, all_server_tasks))
        if len(server_tasks) == 0:
            logging.error("Task %d not found!" % task_id)
            result = False
            continue
        if task != server_tasks[0]:
            logging.error("Task %d does not match!" % task_id)
            result = False
            continue

    return result


def _verify_comments(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    result = True
    # load all comments from dump_task_history
    # if comment parentType = "Task"
    # get all comments from task from server
    # compare
    return result


def _verify_task_lists(ac: ActiveCollab, ac_storage: AcFileStorage) -> bool:
    result = True
    for task_list_id in ac_storage.data_objects["task-lists"].list_ids():
        task_list = ac_storage.data_objects["task-lists"].load(task_list_id)
        project_id = task_list.project_id
        server_all_project_task_lists = []
        try:
            server_all_project_task_lists = ac.get_project_task_lists(
                project_id)
        except Exception as e:
            pass  # ignore exception here
        if len(server_all_project_task_lists) == 0:
            logging.error("No task lists for project %d found!" % project_id)
            result = False
            continue
        server_task_list = list(
            filter(lambda o: o.id == task_list.id,
                   server_all_project_task_lists)
        )
        if len(server_task_list) == 0:
            logging.error(
                "Task list %d for project %d not found!" % (
                    task_list.id, project_id)
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
            filter(lambda c: c.id == project_id, server_projects))
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
            filter(lambda c: c.id == company_id, server_companies))
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
        server_user = list(filter(lambda c: c.id == user_id, server_users))
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

    cnt = _load_companies(ac, ac_storage)
    print("Imported %d companies" % cnt)
    cnt = _load_users(ac, ac_storage)
    print("Imported %d users" % cnt)

    cnt = _load_project_categories(ac, ac_storage)
    print("Imported %d project-category" % cnt)
    cnt = _load_project_labels(ac, ac_storage)
    print("Imported %d project-labels" % cnt)

    cnt = _load_projects(ac, ac_storage)
    print("Imported %d projects" % cnt)
    cnt = _load_task_lists(ac, ac_storage)
    print("Imported %d task-lists" % cnt)
    cnt = _load_tasks(ac, ac_storage)
    print("Imported %d tasks" % cnt)


def _delete_all_tasks(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise Exception("Do not delete data from cloud!")
    for project in ac.get_all_projects():
        ac.delete_all_tasks(project.id)


def _delete_all_task_lists(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise Exception("Do not delete data from cloud!")
    for project in ac.get_all_projects():
        ac.delete_all_task_lists(project)


def _delete_all_projects(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise Exception("Do not delete data from cloud!")
    return ac.delete_all_projects()


def _delete_all_project_categories(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise Exception("Do not delete data from cloud!")
    return ac.delete_all_project_categories()


def _delete_all_project_labels(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise Exception("Do not delete data from cloud!")
    return ac.delete_all_project_labels()


def _delete_all_users(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise Exception("Do not delete data from cloud!")
    return ac.delete_all_users()


def _delete_all_companies(ac: ActiveCollab, config: configparser.ConfigParser):
    if check_is_cloud(config):
        raise Exception("Do not delete data from cloud!")
    return ac.delete_all_companies()


def _load_tasks(ac: ActiveCollab, ac_storage: AcFileStorage) -> int:
    cnt = 0
    for task_id in ac_storage.data_objects["tasks"].list_ids():
        task = ac_storage.data_objects["tasks"].load(task_id)
        if ac.create_task(task):
            cnt += 1
    return cnt


def _load_task_lists(ac: ActiveCollab, ac_storage: AcFileStorage) -> int:
    cnt = 0
    for task_list_id in ac_storage.data_objects["task-lists"].list_ids():
        task_list = ac_storage.data_objects["task-lists"].load(task_list_id)
        if ac.create_task_list(task_list):
            cnt += 1
    return cnt


def _load_projects(ac: ActiveCollab, ac_storage: AcFileStorage) -> int:
    cnt = 0
    for project_id in ac_storage.data_objects["projects"].list_ids():
        project = ac_storage.data_objects["projects"].load(project_id)
        if ac.create_project(project):
            cnt += 1
    return cnt


def _load_project_labels(ac: ActiveCollab, ac_storage: AcFileStorage) -> int:
    cnt = 0
    for project_label_id in ac_storage.data_objects["project-labels"].list_ids():
        project_label = ac_storage.data_objects["project-labels"].load(
            project_label_id)
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


def _load_users(ac: ActiveCollab, ac_storage: AcFileStorage) -> int:
    cnt = 0
    for user_id in ac_storage.data_objects["users"].list_ids():
        user = ac_storage.data_objects["users"].load(user_id)
        if ac.create_user(user):
            cnt += 1
    return cnt


def _load_companies(ac: ActiveCollab, ac_storage: AcFileStorage) -> int:
    cnt = 0
    for company_id in ac_storage.data_objects["companies"].list_ids():
        company = ac_storage.data_objects["companies"].load(company_id)
        if ac.create_company(company):
            cnt += 1
    return cnt


def run(args, parser, config: configparser.ConfigParser):
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
    setup_logging()
    logging.info("Started")
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
    output = run(args, parser, config)
    if isinstance(output, Iterator):
        output = list(output)
    if output is not None:
        print(serialize_output(output))
    logging.info("Finished")


if __name__ == "__main__":
    main()
