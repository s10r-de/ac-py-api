import inspect
import json
import os.path
from unittest import TestCase

from AcCompany import company_from_json
from AcFileStorageCompany import AcFileStorageCompany
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS

DATA_DIR = './data-test/%s/' % __name__
ACCOUNT_ID = 12345


class TestAcFileStorageCompany(TestCase):

    @staticmethod
    def _generate_test_company(company_id: int) -> dict:
        with open('../example-data/example-company-5.json', 'r') as fh:
            company_json = json.load(fh)
        company_json["id"] = company_id
        return company_json

    def test_save(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageCompany(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        company = company_from_json(self._generate_test_company(5))
        filename = storage.save(company)
        self.assertTrue(os.path.isfile(filename))

    def test_save_wrong_class(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageCompany(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        company = company_from_json(self._generate_test_company(50))
        company.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(company)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
