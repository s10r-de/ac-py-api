import configparser
import logging
import os
import shutil
import time

from jinja2 import Environment, FileSystemLoader, select_autoescape

from active_collab_storage.storage import AcFileStorage


def run_html(config: configparser.ConfigParser):
    account_id = config.getint("LOGIN", "account")
    storage_path = config.get("STORAGE", "path")
    ac_storage = AcFileStorage(storage_path, account_id)

    d = os.path.dirname(os.path.abspath(__file__))
    j2env = Environment(
        loader=FileSystemLoader(os.path.join(d, "templates")),
        autoescape=select_autoescape(),
    )
    output_path = config.get("WWW", "path")
    shutil.rmtree(os.path.join(output_path, "*"), ignore_errors=True)
    shutil.copy("css/print.css", output_path)

    data = {}
    data["companies"] = load_all_companies(ac_storage)
    data["project_categories"] = load_all_project_categories(ac_storage)
    data["project_labels"] = load_all_project_labels(ac_storage)

    data["projects"] = load_all_projects(ac_storage)
    data["tasks"] = load_all_tasks(ac_storage)

    render_all_projects(data, j2env, output_path)
    render_all_tasks(data, j2env, output_path)
    return {"path": output_path}

def load_all_projects(ac_storage: AcFileStorage):
    projects = {}
    for project_id in ac_storage.data_objects["projects"].list_ids():
        projects[project_id] = ac_storage.data_objects["projects"].load(project_id)
    return projects

def load_all_companies(ac_storage: AcFileStorage) -> dict:
    companies = {}
    for company_id in ac_storage.data_objects["companies"].list_ids():
        companies[company_id] = ac_storage.data_objects["companies"].load(company_id)
    return companies

def load_all_project_labels(ac_storage: AcFileStorage) -> dict:
    labels = {}
    for label_id in ac_storage.data_objects["project-labels"].list_ids():
        labels[label_id] = ac_storage.data_objects["project-labels"].load(label_id)
    return labels

def load_all_project_categories(ac_storage: AcFileStorage) -> dict:
    categories = {}
    for category_id in ac_storage.data_objects["project-categories"].list_ids():
        categories[category_id] = ac_storage.data_objects["project-categories"].load(category_id)
    return categories

def load_all_tasks(ac_storage: AcFileStorage) -> dict[AcTask]:
    tasks = {}
    for task_id in ac_storage.data_objects["tasks"].list_ids():
        tasks[task_id] = ac_storage.data_objects["tasks"].load(task_id)
    return tasks

def render_all_tasks(data, j2env, output_path):
    for task_id, task in data["tasks"].items():
        task_d = task.to_dict()
        # prepare some variables to be used in template
        task_d["html_filename"] = f"task-{task.id:06d}.html"
        time_format = "%Y-%m-%d"
        task_d["now"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        if task_d["completed_on"]:
            task_d["completed_on"] = time.strftime(
                time_format, time.gmtime(task_d["completed_on"])
            )
        if task_d["created_on"]:
            task_d["created_on"] = time.strftime(
                time_format, time.gmtime(task_d["created_on"])
            )
        if task_d["updated_on"]:
            task_d["updated_on"] = time.strftime(
                time_format, time.gmtime(task_d["updated_on"])
            )
        if task_d["start_on"]:
            task_d["start_on"] = time.strftime(
                time_format, time.gmtime(task_d["start_on"])
            )
        if task_d["due_on"]:
            task_d["due_on"] = time.strftime(
                time_format, time.gmtime(task_d["due_on"])
            )
        out_file = os.path.join(output_path, "task-{}.html".format(task_id))
        html = render_task(j2env, task_d).encode("utf-8")
        save_html(out_file, html)
    # todo: task index?

def render_all_projects(
    data, j2env: Environment, output_path: str
):
    project_list = []
    for project_id, project in data["projects"].items():
        project_d = project.to_dict()

        # add lookup data
        if project.category_id > 0:
            project_d["category"] = data["project_categories"][project.category_id]
        if project.label_id > 0:
            project_d["label"] = data["project_labels"][project.label_id]
        project_d["client_company"] = data["companies"][project.company_id].to_dict()

        # prepare some variables to be used in template
        project_d["html_filename"] = f"project-{project.id:06d}.html"
        time_format = "%Y-%m-%d"
        project_d["now"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        if project_d["completed_on"]:
            project_d["completed_on"] = time.strftime(
                time_format, time.gmtime(project_d["completed_on"])
            )
        if project_d["created_on"]:
            project_d["created_on"] = time.strftime(
                time_format, time.gmtime(project_d["created_on"])
            )
        if project_d["updated_on"]:
            project_d["updated_on"] = time.strftime(
                time_format, time.gmtime(project_d["updated_on"])
            )
        # render and save the HTML
        out_file = os.path.join(output_path, project_d["html_filename"])
        html = render_project(j2env, project_d).encode("utf8")
        save_html(out_file, html)
        project_list.append(project_d)
    save_project_index_html(j2env, output_path, project_list)


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
    project_template = j2env.get_template("project-template.html.j2")
    return project_template.render(**project_d)


def render_project_index(j2env: Environment, project_list: list) -> str:
    project_index_template = j2env.get_template("project-index-template.html.j2")
    return project_index_template.render(projects=project_list)


def render_task(j2env: Environment, task_d: dict) -> str:
    task_template = j2env.get_template("task-template.html.j2")
    return task_template.render(**task_d)
