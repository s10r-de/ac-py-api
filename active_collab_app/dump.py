import configparser

from active_collab_api.active_collab import ActiveCollab
from active_collab_app.statistics import Statistics
from active_collab_app import helper
from active_collab_storage.storage import AcFileStorage

dump_statistics = Statistics()


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

    ac_storage.save_timestamp()
    helper.save_dump_timestamp(config)

    return {
        "account": account_id,
        "storage_path": storage_path,
        "statistics": dump_statistics.get(),
    }


def dump_all_projects_with_all_data(ac, ac_storage):
    for project in ac.get_all_projects():
        ac_storage.data_objects["projects"].save(project)
        dump_statistics.projects.increment()
        dump_all_project_notes(ac, ac_storage, project)
        dump_all_task_lists_of_project(ac, ac_storage, project)
        dump_all_tasks_of_project(ac, ac_storage, project)


def dump_all_project_notes(ac, ac_storage, project):
    for project_note in ac.get_project_notes(project):
        ac_storage.data_objects["project-notes"].save(project_note)
        dump_statistics.project_notes.increment()
        for attachment in project_note.attachments:
            dump_attachment(ac, ac_storage, attachment)


def dump_all_task_lists_of_project(ac, ac_storage, project):
    for task_list in ac.get_project_all_task_lists(project):
        ac_storage.data_objects["task-lists"].save(task_list)
        dump_statistics.task_lists.increment()


def dump_all_tasks_of_project(ac, ac_storage, project):
    for task in ac.get_all_tasks(project.id):
        ac_storage.data_objects["tasks"].save(task)
        dump_statistics.tasks.increment()
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
    dump_statistics.attachments.increment()


def dump_task_comments(ac, ac_storage, task):
    for comment in ac.get_comments(task):
        ac_storage.data_objects["comments"].save(comment)
        dump_statistics.task_comments.increment()
        for attachment in comment.get_attachments():
            dump_attachment(ac, ac_storage, attachment)


def dump_task_history(ac, ac_storage, task):
    for history in ac.get_task_history(task):
        ac_storage.data_objects["task-history"].save(history)
        dump_statistics.task_history.increment()


def dump_task_subtasks(ac, ac_storage, task):
    for subtask in ac.get_subtasks(task):
        ac_storage.data_objects["subtasks"].save(subtask)
        dump_statistics.subtasks.increment()


def dump_all_task_labels(ac, ac_storage):
    for task_label in ac.get_task_labels():
        ac_storage.data_objects["task-labels"].save(task_label)
        dump_statistics.task_labels.increment()


def dump_all_project_labels(ac, ac_storage):
    for project_label in ac.get_project_labels():
        ac_storage.data_objects["project-labels"].save(project_label)
        dump_statistics.project_labels.increment()


def dump_all_project_categories(ac, ac_storage):
    for project_category in ac.get_project_categories():
        ac_storage.data_objects["project-categories"].save(project_category)
        dump_statistics.project_categories.increment()


def dump_all_users(ac, ac_storage):
    for user in ac.get_all_users():
        ac_storage.data_objects["users"].save(user)
        dump_statistics.users.increment()


def dump_all_companies(ac, ac_storage):
    for company in ac.get_all_companies():
        ac_storage.data_objects["companies"].save(company)
        dump_statistics.companies.increment()
