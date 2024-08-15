import json
import os
import shutil

from ActiveCollabAPI.AcProject import AcProject
from ActiveCollabAPI.AcTask import AcTask

DEFAULT_MODE_DIRS = 0o700

class AcFileStorage(object):

    def __init__(self, root_path: str, account_id: int):
        self.root_path = root_path
        self.account_id = account_id

    def reset(self):
        if os.path.exists(self.root_path):
            shutil.rmtree(self.root_path)

    def ensure_dirs(self):
        if not os.path.exists(self.get_account_path()):
            os.makedirs(self.get_account_path(), 0o700)
            os.makedirs(self.get_tasks_path(), 0o700)
            os.makedirs(self.get_account_path(), DEFAULT_MODE_DIRS)
            os.makedirs(self.get_projects_path(), DEFAULT_MODE_DIRS)

    def get_account_path(self) -> str:
        return os.path.join(self.root_path, "account-%08d" % self.account_id)

    def get_tasks_path(self) -> str:
        return os.path.join(self.get_account_path(), "tasks")

    def get_task_filename(self, task: AcTask) -> str:
        return "task-%08d.json" % task.id

    def save_task(self, task: AcTask) -> str:
        assert (task.class_ == "Task")
        task_filename = self.get_task_filename(task)
        task_full_filename = self.get_task_full_filename(task_filename)
        with open(task_full_filename, "w") as f:
            json.dump(task.to_dict(), f, sort_keys=True, indent=2)
        return task_full_filename

    def get_task_full_filename(self, task_filename: str) -> str:
        return os.path.join(self.get_tasks_path(), task_filename)

    def get_projects_path(self) -> str:
        return os.path.join(self.get_account_path(), "projects")

    def get_project_filename(self, project: AcProject) -> str:
        return "project-%08d.json" % project.id

    def get_project_full_filename(self, project_filename: str) -> str:
        return os.path.join(self.get_projects_path(), project_filename)

    def save_project(self, project: AcProject) -> str:
        assert (project.class_ == "Project")
        project_filename = self.get_project_filename(project)
        project_full_filename = self.get_project_full_filename(project_filename)
        with open(project_full_filename, "w") as f:
            json.dump(project.to_dict(), f, sort_keys=True, indent=2)
        return project_full_filename
