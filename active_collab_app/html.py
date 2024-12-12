import configparser
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

from active_collab_api.active_collab import ActiveCollab
from active_collab_storage.storage import AcFileStorage


def run_html(ac: ActiveCollab, config: configparser.ConfigParser):
    account_id = config.getint("LOGIN", "account")
    storage_path = config.get("STORAGE", "path")
    ac_storage = AcFileStorage(storage_path, account_id)

    d = os.path.dirname(os.path.abspath(__file__))
    j2env = Environment(
        loader=FileSystemLoader(os.path.join(d, "templates")),
        autoescape=select_autoescape(),
    )
    return  print_project(ac, ac_storage, j2env)

def print_project(ac: ActiveCollab, ac_storage: AcFileStorage, j2env: Environment):
    project_id = 310
    project = ac_storage.data_objects["projects"].load(project_id)
    project_template = j2env.get_template("project-template.html.j2")
    return project_template.render(**project.to_dict())

