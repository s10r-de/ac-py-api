import json
from unittest import TestCase

from AcCompany import company_from_json, AcCompany
from ActiveCollabAPI import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_


class TestAcCompany(TestCase):

    @staticmethod
    def _generate_test_company(company_id: int) -> AcCompany:
        with open('../example-data/example-company-5.json', 'r') as fh:
            company = company_from_json(json.load(fh))
        company.id = company_id
        return company

    def test_to_dict(self):
        company_id = 7
        company = self._generate_test_company(company_id)
        company_dict = company.to_dict()
        self.assertEqual(company_id, company_dict['id'])
        self.assertIn(AC_PROPERTY_CLASS, company_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, company_dict.keys())

    def test_to_json(self):
        company_id = 7
        company = self._generate_test_company(company_id)
        company_json = company.to_json()
        self.assertEqual(company_id, json.loads(company_json)["id"])
        self.assertIn(AC_PROPERTY_CLASS, json.loads(company_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(company_json).keys())
