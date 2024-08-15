import json
from unittest import TestCase

from ActiveCollabAPI.AcProject import AcProject


class TestAcProject(TestCase):

    def _test_project(self, project_id):
        return AcProject(
            based_on_id=0,
            based_on_type=None,
            body="",
            body_formatted="",
            budget=0.0,
            budget_type="",
            budgeting_interval="",
            category_id=0,
            class_="",
            company_id=0,
            completed_by_id=0,
            completed_on=0,
            count_discussions=0,
            count_files=0,
            count_notes=0,
            count_tasks=0,
            created_by_email="",
            created_by_id=0,
            created_by_name="",
            created_on=0,
            currency_id=0,
            email="",
            file_size=0,
            id=project_id,
            is_billable=False,
            is_client_reporting_enabled=False,
            is_completed=False,
            is_estimate_visible_to_subcontractors=False,
            is_sample=False,
            is_tracking_enabled=False,
            is_trashed=False,
            label_id=0,
            last_activity_on=0,
            leader_id=0,
            members=[1, 2],
            members_can_change_billable=False,
            name="",
            project_number=0,
            show_task_estimates_to_clients=False,
            task_estimates_enabled=False,
            trashed_by_id=0,
            trashed_on=False,
            updated_by_id=0,
            updated_on=0,
            url_path=""
        )

    def test_constructor(self):
        project_id = 554433
        project = self._test_project(project_id)
        self.assertEqual(project.id, project_id)

    def test_to_dict(self):
        project_id = 554433
        project = self._test_project(project_id)
        project_dict = project.to_dict()
        self.assertEqual(project_dict["id"], project_id)

    def test_to_json(self):
        project_id = 554433
        project = self._test_project(project_id)
        project_json = project.to_json()
        self.assertEqual(json.loads(project_json)["id"], project_id)
