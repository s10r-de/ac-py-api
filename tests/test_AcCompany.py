import json
from unittest import TestCase

from active_collab_api.AcCompany import company_from_json
from active_collab_api import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


class TestAcCompany(TestCase):
    @staticmethod
    def _generate_test_company(company_id: int) -> dict:
        with open("tests/example-data/example-company-5.json", "r") as fh:
            company_json = json.load(fh)
        company_json["id"] = company_id
        return company_json

    def test_to_dict(self):
        company_id = 7
        company_json = self._generate_test_company(company_id)
        company = company_from_json(company_json)
        company_dict = company.to_dict()
        self.assertEqual(company_id, company_dict["id"])
        self.assertIn(AC_PROPERTY_CLASS, company_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, company_dict.keys())

    def test_to_json(self):
        company_id = 8
        company_json = self._generate_test_company(company_id)
        company = company_from_json(company_json)
        company_json = company.to_json()
        self.assertEqual(company_id, json.loads(company_json)["id"])
        self.assertIn(AC_PROPERTY_CLASS, json.loads(company_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(company_json).keys())
