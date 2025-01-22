import configparser
import logging
import os
import shutil
import time

from jinja2 import Environment, FileSystemLoader, select_autoescape

from active_collab_api import AC_CLASS_TASK_LIST
from active_collab_api.ac_project import AcProject
from active_collab_api.ac_task_list import AcTaskList
from active_collab_storage.storage import AcFileStorage


def run_html(config: configparser.ConfigParser):
    account_id = config.getint("LOGIN", "account")
    storage_path = config.get("STORAGE", "path")
    ac_storage = AcFileStorage(storage_path, account_id)

    d = os.path.dirname(os.path.abspath(__file__))
    j2env = Environment(
        loader=FileSystemLoader(os.path.join(d, "templates")),
        autoescape=select_autoescape(),
        extensions=['jinja_extension.JinjaFilters']
    )
    output_path = config.get("WWW", "path")
    shutil.rmtree(os.path.join(output_path, "*"), ignore_errors=True)
    shutil.copy("css/print.css", output_path)

    render_all_projects(ac_storage, j2env, output_path)
    render_all_tasks(ac_storage, j2env, output_path)
    return {"path": output_path}

def render_all_tasks(ac_storage: AcFileStorage, j2env: Environment, output_path: str) -> None:
    for task in ac_storage.data_objects["tasks"].get_all():
        task_d = task.to_dict()
        # prepare some variables to be used in template
        task_d["html_filename"] = f"task-{task.id:08d}.html"
        task_d["project"] = ac_storage.data_objects["projects"].load(task.project_id).to_dict()
        task_d["subtasks"] = map(lambda t: t.to_dict(),
                                 ac_storage.data_objects["subtasks"].sort_by_position(
                                     ac_storage.data_objects["subtasks"].find_by_task(task.id)))
        # render and save the HTML
        out_file = os.path.join(output_path, task_d["html_filename"])
        html = render_task(j2env, task_d).encode("utf-8")
        save_html(out_file, html)
    # todo: task index?

def render_all_projects(
    ac_storage: AcFileStorage, j2env: Environment, output_path: str
) -> None:
    project_list = []
    for project in ac_storage.data_objects["projects"].get_all():
        project_d = render_one_project(ac_storage, j2env, output_path, project)
        project_list.append(project_d)
    save_project_index_html(j2env, output_path, project_list)


def render_one_project(ac_storage, j2env, output_path, project):
    project_d = project.to_dict()
    project_d["html_filename"] = f"project-{project.id:08d}.html"
    # add lookup data
    if project.category_id > 0:
        project_d["category"] = (
            ac_storage.data_objects["project-categories"].load(project.category_id).to_dict())
    if project.label_id > 0:
        project_d["label"] = (
            ac_storage.data_objects["project-labels"].load(project.label_id).to_dict())
    project_d["client_company"] = (
        ac_storage.data_objects["companies"].load(project.company_id).to_dict())
    project_d["members"] = prepare_project_members(ac_storage, project)
    project_d["task_lists"] = prepare_project_task_lists(ac_storage, project)
    project_d["tasks_by_tasklist"] = {}
    for tasklist in project_d["task_lists"]:
        project_d["tasks_by_tasklist"][tasklist["id"]] = (
            prepare_tasklist_tasks(ac_storage, tasklist["id"]))
    project_d["tasks_without_task_lists"] = prepare_tasklist_tasks(ac_storage, 0)
    # render and save the HTML
    out_file = os.path.join(output_path, project_d["html_filename"])
    html = render_project(j2env, project_d).encode("utf8")
    save_html(out_file, html)
    return project_d

def task_list_without_tasks() -> AcTaskList:
    return AcTaskList(
        class_ = AC_CLASS_TASK_LIST,
        completed_by_id=None,
        completed_on=0,
        completed_tasks=0,
        created_by_email="",
        created_by_id=0,
        created_by_name="",
        created_on=0,
        due_on=0,
        id=0,
        is_completed=True,
        is_trashed=False,
        name="Tasks without task list",
        open_tasks=0,
        position=999999,
        project_id=0,
        start_on=0,
        trashed_by_id=0,
        trashed_on=0,
        updated_by_id=0,
        updated_on=0,
        url_path=""
    )

def prepare_project_task_lists(ac_storage, project: AcProject):
    task_lists = []
    task_lists.append(task_list_without_tasks())
    task_lists.extend(list(ac_storage.data_objects["task-lists"].find_by_project(project.id)))
    # TODO: sort by position
    return list(map(lambda t: t.to_dict(), task_lists))

def prepare_project_tasks(ac_storage, project: AcProject) -> list[dict]:
    return list(map(lambda t: t.to_dict(),
                    ac_storage.data_objects["tasks"].find_by_project(project.id)))

def prepare_tasklist_tasks(ac_storage, tasklist_id: int) -> list[dict]:
    # TODO: sort by position
    return list(map(lambda t: t.to_dict(),
                    ac_storage.data_objects["tasks"].find_by_tasklist(tasklist_id)))



def prepare_project_members(ac_storage, project):
    members = []
    for member_id in project.members:
        try:
            user = ac_storage.data_objects["users"].load(member_id)
            members.append(user.to_dict())
        except FileNotFoundError as _e:
            logging.error("User '%s' not found" % member_id)
    return members


def save_project_index_html(j2env, output_path, project_list):
    index_file = os.path.join(output_path, "index.html")
    logging.debug("write %s" % index_file)
    with open(index_file, "w", encoding="utf-8") as f1:
        f1.write(render_project_index(j2env, project_list))
        f1.close()


def save_html(out_file, html):
    logging.debug("write %s" % out_file)
    with open(out_file, "wb") as fp:
        fp.write(html)
        fp.close()


def render_project(j2env: Environment, project_d: dict) -> str:
    context = {
        'now': time.time()
    }
    project_template = j2env.get_template("project-template.html.j2")
    return project_template.render(**project_d, **context)


def render_project_index(j2env: Environment, project_list: list) -> str:
    context = {
        'now': time.time()
    }
    project_index_template = j2env.get_template("project-index-template.html.j2")
    return project_index_template.render(projects=project_list, **context)


def render_task(j2env: Environment, task_d: dict) -> str:
    context = {
        'now': time.time()
    }
    task_template = j2env.get_template("task-template.html.j2")
    return task_template.render(**task_d, **context)
