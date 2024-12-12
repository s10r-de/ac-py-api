import configparser
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
    render_all_projects(ac_storage, j2env, output_path)


def render_all_projects(
    ac_storage: AcFileStorage, j2env: Environment, output_path: str
):
    project_list = []
    for project_id in ac_storage.data_objects["projects"].list_ids():
        project = ac_storage.data_objects["projects"].load(project_id)
        project_d = project.to_dict()
        # prepare some variables to be used in template
        project_d["html_filename"] = f"project-{project.id:06d}.html"
        # FIXME: gmtime() or localtime() ??
        time_format = "%Y-%m-%d %H:%M:%S"
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
    with open(index_file, "w", encoding="utf-8") as f1:
        f1.write(render_project_index(j2env, project_list))
        f1.close()


def save_html(out_file, html):
    with open(out_file, "wb") as fp:
        fp.write(html)
        fp.close()


def render_project(j2env: Environment, project_d: dict) -> str:
    project_template = j2env.get_template("project-template.html.j2")
    return project_template.render(**project_d)


def render_project_index(j2env: Environment, project_list: list) -> str:
    project_index_template = j2env.get_template("project-index-template.html.j2")
    return project_index_template.render(projects=project_list)
