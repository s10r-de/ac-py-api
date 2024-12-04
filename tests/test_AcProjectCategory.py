import json
import time
from unittest import TestCase

from active_collab_api.AcProjectCategory import AcProjectCategory
from active_collab_api import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


class TestAcProjectCategory(TestCase):
    @staticmethod
    def _generate_test_project_category(category_id: int) -> AcProjectCategory:
        return AcProjectCategory(
            class_="ProjectCategory",
            created_by_email="admin@example.com",
            created_by_id=2,
            created_by_name="the creator",
            created_on=int(time.time()),
            id=category_id,
            name="Test Project Category",
            parent_id=None,
            parent_type=None,
            updated_on=int(time.time()) + 2,
            url_path="/categories/%d" % category_id,
        )

    def test_constructor(self):
        category_id = 735
        category = self._generate_test_project_category(category_id)
        self.assertEqual(category_id, category.id)

    def test_to_dict(self):
        category_id = 736
        category = self._generate_test_project_category(category_id)
        category_dict = category.to_dict()
        self.assertEqual(category_id, category_dict["id"])
        self.assertEqual(
            "ProjectCategory",
            category_dict["class"],
        )
        self.assertIn(AC_PROPERTY_CLASS, category_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, category_dict.keys())

    def test_to_json(self):
        category_id = 737
        category = self._generate_test_project_category(category_id)
        category_json = category.to_json()
        self.assertEqual(category_id, json.loads(category_json)["id"])
        self.assertEqual(
            "ProjectCategory",
            json.loads(category_json)["class"],
        )
        self.assertIn(AC_PROPERTY_CLASS, json.loads(category_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(category_json).keys())
