class Counter:

    def __init__(self, initial=0):
        self.initial = initial
        self.counter = initial

    def reset(self):
        self.counter = self.initial

    def increment(self):
        self.counter += 1

    def get(self) -> int:
        return self.counter


class Statistics:
    attachments = Counter()
    companies = Counter()
    project_categories = Counter()
    project_labels = Counter()
    project_notes = Counter()
    projects = Counter()
    subtasks = Counter()
    task_comments = Counter()
    task_history = Counter()
    task_labels = Counter()
    task_lists = Counter()
    tasks = Counter()
    users = Counter()

    def get(self) -> dict:
        return {
            "attachments": self.attachments.get(),
            "companies": self.companies.get(),
            "project_categories": self.project_categories.get(),
            "project_labels": self.project_labels.get(),
            "project_notes": self.project_notes.get(),
            "projects": self.projects.get(),
            "subtasks": self.subtasks.get(),
            "task_comments": self.task_comments.get(),
            "task_history": self.task_history.get(),
            "task_labels": self.task_labels.get(),
            "task_lists": self.task_lists.get(),
            "tasks": self.tasks.get(),
            "users": self.users.get(),
        }
