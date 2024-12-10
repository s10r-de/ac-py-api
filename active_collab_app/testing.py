import configparser

from active_collab_api import AC_CLASS_TASK
from active_collab_api.ac_task import AcTask
from active_collab_api.active_collab import ActiveCollab


def run_testing(ac: ActiveCollab, config: configparser.ConfigParser):  # pylint: disable=unused-argument
    # account_id = config.getint("LOGIN", "account")
    # storage_path = config.get("STORAGE", "path")
    # ac_storage = AcFileStorage(storage_path, account_id)

    result = []

    # https://ac-backup.[example].de/projects/745?modal=Task-37180-745
    project_id = 745
    task_id = 37180
    task_number = 1629

    task = AcTask(project_id=project_id,
                  id=task_id,
                  task_number=task_number,
                  assignee_id=0,
                  attachments=[],
                  body="",
                  body_formatted="",
                  body_mode="",
                  class_=AC_CLASS_TASK,
                  comments_count=0,
                  completed_by_id=0,
                  completed_on=0,
                  completed_subtasks=0,
                  created_by_email="",
                  created_by_id=0,
                  created_by_name="",
                  created_from_recurring_task_id=0,
                  created_on=0,
                  delegated_by_id=0,
                  due_on=0,
                  estimate=0,
                  fake_assignee_email="",
                  fake_assignee_name="",
                  is_billable=False,
                  is_completed=False,
                  is_hidden_from_clients=False,
                  is_important=False,
                  is_trashed=False,
                  job_type_id=0,
                  labels=[],
                  name="",
                  open_dependencies=None,
                  open_subtasks=0,
                  position=0,
                  start_on=0,
                  task_list_id=0,
                  total_subtasks=0,
                  trashed_by_id=0,
                  trashed_on=0,
                  updated_by_id=0,
                  updated_on=0,
                  url_path="")
    result = ac.update_task_set_task_number(task)

    return result
    # return map(lambda r: r.to_dict(), result)
