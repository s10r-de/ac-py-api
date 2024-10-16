import argparse
import configparser
import json
from collections.abc import Iterator

from AcStorage.AcFileStorage import AcFileStorage
from ActiveCollabAPI.ActiveCollab import ActiveCollab


def load_config(args):
    config = configparser.ConfigParser()
    config.read(args.config)
    return config


def serialize_output(output):
    # serialize the output
    return json.dumps(output, indent=4)


def run_testing(ac, config: configparser.ConfigParser):
    account_id = config.getint('LOGIN', 'account')
    storage_path = config.get('STORAGE', 'path')
    ac_storage = AcFileStorage(storage_path, account_id)
    return ac_storage.data_objects["task-history"].list()


def run_version():
    from version import VERSION
    return {"version": VERSION}


def run_info(ac: ActiveCollab):
    return ac.get_info()


def run_dump_all(ac: ActiveCollab, config: configparser.ConfigParser):
    account_id = config.getint('LOGIN', 'account')
    storage_path = config.get('STORAGE', 'path')

    ac_storage = AcFileStorage(storage_path, account_id)
    ac_storage.reset()
    ac_storage.ensure_dirs()

    dump_all_companies(ac, ac_storage)
    dump_all_users(ac, ac_storage)
    dump_all_project_categories(ac, ac_storage)
    dump_all_project_labels(ac, ac_storage)
    dump_all_task_labels(ac, ac_storage)
    dump_all_projects_with_all_data(ac, ac_storage)

    return {'message': "data of account %d dumped to %s" % (account_id, storage_path)}

    # get tasks modified after 1723452690  12.08.2024 10:51 CEST
    # tasks = ac.filter_tasks(tasks, lambda t: t.updated_on > 1723452690)
    # tasks = ac.filter_tasks(tasks, lambda t: t.id == 18440)
    # return list(map(lambda task: task.to_dict(), projects))


def dump_all_projects_with_all_data(ac, ac_storage):
    projects = ac.get_active_projects()
    projects.extend(ac.get_archived_projects())
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
    for task_list in ac.get_project_task_lists(project):
        ac_storage.data_objects["task-lists"].save(task_list)


def dump_all_tasks_of_project(ac, ac_storage, project):
    tasks = ac.get_active_tasks(project.id)
    tasks.extend(ac.get_completed_tasks(project.id))
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
    ac_storage.data_objects["attachments"].save(attachment, ac.download_attachment(attachment))


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
    ac.login(
        config.get("LOGIN", "username"),
        config.get("LOGIN", "password"),
        account
    )
    return ac


def run_load_all(ac: ActiveCollab, config: configparser.ConfigParser):
    account_id = config.getint('LOGIN', 'account')
    storage_path = config.get('STORAGE', 'path')
    ac_storage = AcFileStorage(storage_path, account_id)

    cnt = 0
    for company_id in ac_storage.data_objects["companies"].list_ids():
        company = ac_storage.data_objects["companies"].load(company_id)
        if ac.create_company(company):
            cnt += 1
    print("Imported %d companies" % cnt)

    cnt = 0
    for user_id in ac_storage.data_objects["users"].list_ids():
        user = ac_storage.data_objects["users"].load(user_id)
        if ac.create_user(user):
            cnt += 1
    print("Imported %d users" % cnt)

    cnt = 0
    for project_category_id in ac_storage.data_objects["project-categories"].list_ids():
        project_category = ac_storage.data_objects["project-categories"].load(project_category_id)
        if ac.create_project_category(project_category):
            cnt += 1
    print("Imported %d project-category" % cnt)


def run(args, parser, config: configparser.ConfigParser):
    # run the commands
    if args.command == 'version':
        return run_version()
    if args.command == 'info':
        return run_info(_login(config))
    if args.command == 'dump':
        return run_dump_all(_login(config), config)
    if args.command == 'load':
        return run_load_all(_login(config), config)
    if args.command == "testing":
        return run_testing(_login(config), config)

    # no command given so show the help
    parser.print_help()
    return None


def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        prog='acdump',
        description='This is a tool to dump data from Active-Collab',
        epilog='(c) 2024 by ACME VC, Charlie Sloan <cs@example.com>')
    parser.add_argument('-c', '--config', required=True,
                        help="use the named config file")
    parser.add_argument('command', choices=['version', 'info', 'dump', 'load', 'testing'],
                        help='The command to run')
    args = parser.parse_args()
    config = load_config(args)
    output = run(args, parser, config)
    if isinstance(output, Iterator):
        output = list(output)
    if output is not None:
        print(serialize_output(output))


if __name__ == "__main__":
    main()
