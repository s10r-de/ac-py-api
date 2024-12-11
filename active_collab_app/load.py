import configparser
import logging

from active_collab_api import AC_CLASS_USER_OWNER, AC_CLASS_USER_MEMBER
from active_collab_api.ac_project import AcProject
from active_collab_api.ac_subtask import AcSubtask
from active_collab_api.ac_task import AcTask
from active_collab_api.ac_task_list import AcTaskList
from active_collab_api.ac_user import AcUser
from active_collab_api.active_collab import ActiveCollab
from active_collab_app.helper import map_user_id, map_company_id
from active_collab_app.statistics import Statistics
from active_collab_storage.storage import AcFileStorage

load_statistics = Statistics()
load_success_statistics = Statistics()
load_completed_statistics = Statistics()


def run_load_all(ac: ActiveCollab, config: configparser.ConfigParser):
    global load_statistics, load_completed_statistics, load_success_statistics
    account_id = config.getint("LOGIN", "account")
    storage_path = config.get("STORAGE", "path")
    ac_storage = AcFileStorage(storage_path, account_id)

    load_companies(ac, ac_storage)  # TODO: archived companies
    archived_users = load_users(config, ac, ac_storage)

    load_project_categories(ac, ac_storage)  # TODO: archived categories
    load_project_labels(ac, ac_storage)  # TODO: archived labels

    complete_projects = load_projects(config, ac, ac_storage)
    complete_task_lists = load_task_lists(ac, ac_storage)
    complete_tasks = load_tasks(ac, ac_storage)
    complete_subtasks = load_subtasks(ac, ac_storage)

    load_comments(ac, ac_storage)  # TODO: archived comments?
    load_attachments(ac, ac_storage)  # TODO: archived attachments?

    for subtask in complete_subtasks:
        ac.complete_subtask(subtask)
        load_completed_statistics.subtasks.increment()
    for task in complete_tasks:
        ac.complete_task(task)
        load_completed_statistics.tasks.increment()
    for task_list in complete_task_lists:
        ac.complete_task_list(task_list)
        load_completed_statistics.task_lists.increment()
    for project in complete_projects:
        ac.complete_project(project)
        load_completed_statistics.projects.increment()
    for user in archived_users:
        ac.archive_user(user)
        load_completed_statistics.users.increment()

    return {
        "all": load_statistics.get(),
        "success": load_success_statistics.get(),
        "completed": load_completed_statistics.get()
    }


def load_project_labels(ac: ActiveCollab, ac_storage: AcFileStorage) -> None:
    global load_statistics, load_success_statistics
    for project_label_id in ac_storage.data_objects["project-labels"].list_ids():
        project_label = ac_storage.data_objects["project-labels"].load(project_label_id)
        load_statistics.project_labels.increment()
        if ac.create_project_label(project_label):
            load_success_statistics.project_labels.increment()


def load_project_categories(ac: ActiveCollab, ac_storage: AcFileStorage) -> None:
    global load_statistics, load_success_statistics
    for project_category_id in ac_storage.data_objects["project-categories"].list_ids():
        project_category = ac_storage.data_objects["project-categories"].load(
            project_category_id
        )
        load_statistics.project_categories.increment()
        if ac.create_project_category(project_category):
            load_success_statistics.project_categories.increment()


def load_users(
    config: configparser.ConfigParser, ac: ActiveCollab, ac_storage: AcFileStorage
) -> list[AcUser]:
    global load_statistics, load_success_statistics
    archived = []
    for user_id in ac_storage.data_objects["users"].list_ids():
        archived_user = None
        user = ac_storage.data_objects["users"].load(user_id)
        load_statistics.users.increment()
        user.company_id = map_company_id(config, user.company_id)
        if user.is_archived:
            archived_user = user
            user.is_archived = False
        if user.class_ == AC_CLASS_USER_OWNER:
            user.class_ = AC_CLASS_USER_MEMBER
        if ac.create_user(user):
            if archived_user:
                archived.append(archived_user)
            load_success_statistics.users.increment()
    return archived


def load_companies(ac: ActiveCollab, ac_storage: AcFileStorage) -> None:
    global load_statistics, load_success_statistics
    for company_id in ac_storage.data_objects["companies"].list_ids():
        company = ac_storage.data_objects["companies"].load(company_id)
        load_statistics.companies.increment()
        if ac.create_company(company):
            load_success_statistics.companies.increment()


def load_attachments(ac: ActiveCollab, ac_storage: AcFileStorage) -> None:
    global load_statistics, load_success_statistics
    for attachment_id in ac_storage.data_objects["attachments"].list_ids():
        attachment = ac_storage.data_objects["attachments"].load(attachment_id)
        load_statistics.attachments.increment()
        bin_file = ac_storage.data_objects["attachments"].get_bin_filename(attachment)
        logging.debug("Uploading file %s" % bin_file)
        if ac.upload_attachment(attachment, bin_file):
            load_success_statistics.attachments.increment()


def load_comments(ac: ActiveCollab, ac_storage: AcFileStorage) -> None:
    global load_statistics, load_success_statistics
    for comment_id in ac_storage.data_objects["comments"].list_ids():
        comment = ac_storage.data_objects["comments"].load(comment_id)
        load_statistics.task_comments.increment()
        if ac.create_comment(comment):
            load_success_statistics.task_comments.increment()


def load_subtasks(ac: ActiveCollab, ac_storage: AcFileStorage) -> list[AcSubtask]:
    global load_statistics, load_success_statistics
    completed = []
    for subtask_id in ac_storage.data_objects["subtasks"].list_ids():
        add_to_completed = None
        subtask = ac_storage.data_objects["subtasks"].load(subtask_id)
        load_statistics.subtasks.increment()
        if subtask.is_completed:
            add_to_completed = subtask
            subtask.is_completed = False
            subtask.completed_by_id = None
            subtask.completed_on = None
        if ac.create_subtask(subtask):
            if add_to_completed:
                completed.append(add_to_completed)
            load_success_statistics.subtasks.increment()
    return completed


def load_tasks(ac: ActiveCollab, ac_storage: AcFileStorage) -> list[AcTask]:
    global load_statistics, load_success_statistics
    completed = []
    for task_id in ac_storage.data_objects["tasks"].list_ids():
        add_to_completed = None
        task = ac_storage.data_objects["tasks"].load(task_id)
        load_statistics.tasks.increment()
        if task.is_completed:
            add_to_completed = task
            task.is_completed = False
            task.completed_by_id = None
            task.completed_on = None
        if ac.create_task(task):
            if add_to_completed:
                completed.append(add_to_completed)
            load_success_statistics.tasks.increment()
    fix_task_number(ac, ac_storage, 10000)
    fix_task_number(ac, ac_storage)
    return completed


def fix_task_number(ac: ActiveCollab, ac_storage: AcFileStorage, offset: int = 0) -> None:
    tasks = ac_storage.data_objects["tasks"].list_ids()
    if tasks is None:
        return
    tasks.reverse()
    for task_id in tasks:
        task = ac_storage.data_objects["tasks"].load(task_id)
        task.task_number = task.task_number + offset
        ac.update_task_set_task_number(task)


def load_task_lists(ac: ActiveCollab, ac_storage: AcFileStorage) -> list[AcTaskList]:
    global load_statistics, load_success_statistics
    completed = []
    for task_list_id in ac_storage.data_objects["task-lists"].list_ids():
        add_to_completed = None
        task_list = ac_storage.data_objects["task-lists"].load(task_list_id)
        load_statistics.task_lists.increment()
        if task_list.is_completed:
            add_to_completed = task_list
            task_list.is_completed = False
            task_list.completed_by_id = None
            task_list.completed_on = None
            task_list.open_tasks = 0
        if ac.create_task_list(task_list):
            if add_to_completed:
                completed.append(add_to_completed)
            load_success_statistics.task_lists.increment()
    return completed


def load_projects(
    config: configparser.ConfigParser, ac: ActiveCollab, ac_storage: AcFileStorage
) -> list[AcProject]:
    global load_statistics, load_success_statistics
    completed = []
    for project_id in ac_storage.data_objects["projects"].list_ids():
        add_to_completed = None
        project = ac_storage.data_objects["projects"].load(project_id)
        load_statistics.projects.increment()
        project.company_id = map_company_id(config, project.company_id)
        project.members = list(map(lambda uid, cfg=config: map_user_id(cfg, uid), project.members))
        if project.is_completed:
            add_to_completed = project
            project.is_completed = False
            project.completed_on = None
            project.completed_by_id = None
        if ac.create_project(project):
            if add_to_completed:
                completed.append(add_to_completed)
            load_success_statistics.projects.increment()
    fix_project_number(ac, ac_storage, 10000)
    fix_project_number(ac, ac_storage)
    return completed


def fix_project_number(ac: ActiveCollab, ac_storage: AcFileStorage, offset: int = 0) -> None:
    projects = ac_storage.data_objects["projects"].list_ids()
    if projects is None:
        return
    projects.reverse()
    for project_id in projects:
        project = ac_storage.data_objects["projects"].load(project_id)
        project.project_number = project.project_number + offset
        ac.update_project_set_project_number(project)
