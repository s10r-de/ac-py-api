import inspect
import json
import os.path
from unittest import TestCase

from active_collab_api import AC_ERROR_WRONG_CLASS
from active_collab_api.ac_company import company_from_json
from active_collab_storage.company import AcFileStorageCompany

DATA_DIR = f"./data-test/{__name__}/"
ACCOUNT_ID = 12345


class TestCompany(TestCase):
    @staticmethod
    def _generate_test_company(company_id: int) -> dict:
        with open(
            "tests/example-data/example-company-5.json", "r", encoding="utf-8"
        ) as fh:
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

    def test_list_ids(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageCompany(DATA_DIR + m_name, ACCOUNT_ID)
        storage.reset()
        storage.ensure_dirs()
        ids = storage.list_ids()
        with self.assertRaises(StopIteration):
            next(ids)
        company = company_from_json(self._generate_test_company(5))
        storage.save(company)
        ids = storage.list_ids()
        item_id = next(ids)
        self.assertEqual(5, item_id)
        company = company_from_json(self._generate_test_company(6))
        storage.save(company)
        ids = storage.list_ids()
        next(ids)
        item_id = next(ids)
        self.assertEqual(6, item_id)
        storage.save(company)  # overwrite!
        ids = storage.list_ids()
        next(ids)
        item_id = next(ids)
        self.assertEqual(6, item_id)
        with self.assertRaises(StopIteration):
            next(ids)
