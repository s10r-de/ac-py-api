import json
from unittest import TestCase

from active_collab_api import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_
from active_collab_api.ac_attachment import AcAttachment, attachment_from_json
from active_collab_api.ac_task import AcTask, task_from_json
from active_collab_api.ac_task_dependencies import AcTaskDependencies


class TestAcTask(TestCase):
    @staticmethod
    def _generate_test_task(task_id: int) -> AcTask:
        with open(
            "tests/example-data/example-task-17614.json", "r", encoding="utf-8"
        ) as fh:
            task = task_from_json(json.load(fh))
        task.id = task_id
        return task

    @staticmethod
    def _generate_test_attachment(attachment_id: int) -> AcAttachment:
        with open(
            "tests/example-data/example-attachment-29703.json", "r", encoding="utf-8"
        ) as fh:
            attachment = attachment_from_json(json.load(fh))
        attachment.id = attachment_id
        return attachment

    def test_actask_constructor(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        self.assertEqual(task_id, task.id)

    def test_to_dict(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        task_dict = task.to_dict()
        self.assertEqual(task_id, task_dict["id"])
        self.assertIn(AC_PROPERTY_CLASS, task_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, task_dict.keys())

    def test_to_json(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        task_json = task.to_json()
        self.assertEqual(task_id, json.loads(task_json)["id"])
        self.assertIn(AC_PROPERTY_CLASS, json.loads(task_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(task_json).keys())

    def test_to_dict_with_dependencies(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        task.open_dependencies = AcTaskDependencies(parents_count=2, children_count=3)
        task.attachments = []
        task_dict = task.to_dict()
        self.assertEqual(task_id, task_dict["id"])
        self.assertEqual(2, task_dict["open_dependencies"]["parents_count"])
        self.assertEqual(3, task_dict["open_dependencies"]["children_count"])

    def test_to_json_with_dependencies(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        task.open_dependencies = AcTaskDependencies(parents_count=2, children_count=3)
        task.attachments = []
        task_json = task.to_json()
        parsed_json = json.loads(task_json)
        self.assertEqual(task_id, parsed_json["id"])
        self.assertEqual(2, parsed_json["open_dependencies"]["parents_count"])
        self.assertEqual(3, parsed_json["open_dependencies"]["children_count"])

    def test_get_attachments(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        task.open_dependencies = None
        task.attachments = [
            self._generate_test_attachment(78),
            self._generate_test_attachment(79),
        ]
        attachments = task.get_attachments()
        self.assertEqual(2, len(attachments))
        self.assertIsInstance(attachments[0], AcAttachment)
        self.assertIsInstance(attachments[1], AcAttachment)

    def test_to_dict_with_attachments(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        task.open_dependencies = None
        task.attachments = [
            self._generate_test_attachment(78),
            self._generate_test_attachment(79),
        ]
        task_dict = task.to_dict()
        self.assertEqual(task_id, task_dict["id"])
        self.assertEqual(2, len(task_dict["attachments"]))
        self.assertEqual(task_dict["attachments"][0]["class"], "WarehouseAttachment")
        self.assertEqual(task_dict["attachments"][1]["class"], "WarehouseAttachment")

    def test_to_json_with_attachments(self):
        task_id = 17614
        task = self._generate_test_task(task_id)
        task.open_dependencies = None
        task.attachments = [
            self._generate_test_attachment(78),
            self._generate_test_attachment(79),
        ]
        task_json = task.to_json()
        parsed_json = json.loads(task_json)
        self.assertEqual(task_id, parsed_json["id"])
        self.assertEqual(2, len(parsed_json["attachments"]))
        self.assertEqual(parsed_json["attachments"][0]["class"], "WarehouseAttachment")
        self.assertEqual(parsed_json["attachments"][1]["class"], "WarehouseAttachment")

    @staticmethod
    def _generate_test_task_with_attachments(task_id: int) -> AcTask:
        with open(
            "tests/example-data/example-task-17614b.json", "r", encoding="utf-8"
        ) as fh:
            task = task_from_json(json.load(fh))
        task.id = task_id
        return task

    def test_from_json_with_attachments(self):
        task_id = 17614
        task = self._generate_test_task_with_attachments(task_id)
        attachments = task.get_attachments()
        self.assertEqual(2, len(attachments))
        self.assertIsInstance(attachments[0], AcAttachment)
        self.assertIsInstance(attachments[1], AcAttachment)
