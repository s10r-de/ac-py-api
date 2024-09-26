import json
from unittest import TestCase

from AcCompany import company_from_json, AcCompany


class TestAcCompany(TestCase):

    def _generate_test_company(self, company_id: int) -> AcCompany:
        with open('../example-data/example-company-5.json', 'r') as fh:
            company = company_from_json(json.load(fh))
        company.id = company_id
        return company

    def test_to_dict(self):
        company_id = 7
        company = self._generate_test_company(company_id)
        company_dict = company.to_dict()
        self.assertEqual(company_dict['id'], company_id)

    def test_to_json(self):
        company_id = 7
        company = self._generate_test_company(company_id)
        company_json = company.to_json()
        self.assertEqual(json.loads(company_json)["id"], company_id)
