import glob
import locale
import os

from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcTaskHistory import AcTaskHistory


class AcFileStorageTaskHistory(AcFileStorageBaseClass):
    filename_prefix = "task-history"
    dir_name = "task-history"

    def make_id(self, task_id, timestamp):
        return task_id + (timestamp / 10 ** 10)

    def parse_id(self, id_with_ts: float):
        id = int(id_with_ts)
        ts = (id_with_ts - id) * 10 ** 10
        return (id, ts)

    def save(self, task_history: AcTaskHistory) -> str:
        def id_from_task_history(task_history):
            return "task-history-%08.10f.json" % self.make_id(task_history.task_id, task_history.timestamp)

        return super().save(task_history, id=id_from_task_history(task_history))

    def list(self):
        # strip path and "${filename_prefix}-" and ".json"
        n = len(self.filename_prefix)

        # id is a float - <task_id>.<timestamp>
        def extract_number(f):
            id = locale.atof(os.path.basename(f)[n + 1:-5])
            return id

        return map(extract_number,
                   glob.iglob(os.path.join(self.get_path(), self.filename_prefix + "-*.json")))
