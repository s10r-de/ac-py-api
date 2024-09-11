import argparse
import configparser
import json

from AcStorage.AcFileStorage import AcFileStorage
from ActiveCollabAPI.ActiveCollab import ActiveCollab


def load_config(args):
    config = configparser.ConfigParser()
    config.read(args.config)
    return config


def serialize_output(output):
    # serialize the output
    return json.dumps(output, indent=4)


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

    # get all users
    users = ac.get_all_users()
    for user in users:
        ac_storage.save_user(user)

    # get all projects
    projects = ac.get_active_projects()
    projects.extend(ac.get_archived_projects())
    for project in projects:
        ac_storage.save_project(project)
        # get all tasks for this project
        tasks = ac.get_active_tasks(project.id)
        tasks.extend(ac.get_completed_tasks(project.id))
        for task in tasks:
            ac_storage.save_task(task)
            if task.total_subtasks > 0:
                subtasks = ac.get_subtasks(task)
                for subtask in subtasks:
                    ac_storage.save_subtask(subtask)
            if task.comments_count > 0:
                comments = ac.get_comments(task)
                for comment in comments:
                    ac_storage.save_comment(comment)


    return {'message': "data of account %d dumped to %s" % (account_id, storage_path)}

    # get tasks modified after 1723452690  12.08.2024 10:51 CEST
    # tasks = ac.filter_tasks(tasks, lambda t: t.updated_on > 1723452690)
    # tasks = ac.filter_tasks(tasks, lambda t: t.id == 18440)
    # return list(map(lambda task: task.to_dict(), projects))


def _login(config: configparser.ConfigParser) -> ActiveCollab:
    # create the AC Client
    base_url = config.get("DEFAULT", "base_url")
    ac = ActiveCollab(base_url)
    ac.login_to_account(
        config.get("LOGIN", "username"),
        config.get("LOGIN", "password"),
        config.get("LOGIN", "account", fallback=None)
    )
    return ac


def run(args, parser, config: configparser.ConfigParser):
    # run the commands
    if args.version:
        return run_version()
    if args.info:
        return run_info(_login(config))
    if args.dump:
        return run_dump_all(_login(config), config)

    # no command given so show the help
    parser.print_help()
    return None


def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        prog='acdump',
        description='This is a tool to dump data from Active-Collab',
        epilog='(c) 2024 by ACME VC, Charlie Sloan <cs@example.com>')
    parser.add_argument('-v', '--version', action='store_true',
                        help="show version information for this tool", default=False)
    parser.add_argument('-c', '--config', required=True,
                        help="use the named config file")
    parser.add_argument('--info', action='store_true',
                        help="show server information", default=False)
    parser.add_argument('--dump', action='store_true',
                        help="dump all data", default=False)
    args = parser.parse_args()
    config = load_config(args)
    output = run(args, parser, config)
    if output is not None:
        print(serialize_output(output))


if __name__ == "__main__":
    main()
