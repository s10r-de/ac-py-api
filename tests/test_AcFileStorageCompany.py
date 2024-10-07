import json
import os.path
from unittest import TestCase

from AcCompany import company_from_json
from AcFileStorageCompany import AcFileStorageCompany
from ActiveCollabAPI import AC_ERROR_WRONG_CLASS

DATA_DIR = './data'
ACCOUNT_ID = 12345


class TestAcFileStorageCompany(TestCase):

    @staticmethod
    def _generate_test_company(company_id: int) -> dict:
        with open('../example-data/example-company-5.json', 'r') as fh:
            company_json = json.load(fh)
        company_json["id"] = company_id
        return company_json

    def test_get_path(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageCompany(DATA_DIR, account_id)
        self.assertGreater(len(storage.get_path()), 1)

    def test_reset(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageCompany(DATA_DIR, account_id)
        storage.reset()
        self.assertFalse(os.path.isdir(storage.get_path()))

    def test_ensure_dirs(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageCompany(DATA_DIR, account_id)
        storage.ensure_dirs()
        self.assertTrue(os.path.isdir(storage.get_path()))

    def test_get_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageCompany(DATA_DIR, account_id)
        company = company_from_json(self._generate_test_company(5))
        filename = storage.get_filename(company)
        self.assertGreater(len(filename), 0)

    def test_get_full_filename(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageCompany(DATA_DIR, account_id)
        company = company_from_json(self._generate_test_company(5))
        filename = storage.get_filename(company)
        full_filename = storage.get_full_filename(filename)
        self.assertGreater(len(full_filename), 0)

    def test_save(self):
        account_id = ACCOUNT_ID
        storage = AcFileStorageCompany(DATA_DIR, account_id)
        storage.reset()
        storage.ensure_dirs()
        company = company_from_json(self._generate_test_company(5))
        full_filename = storage.save(company)
        self.assertGreater(len(full_filename), 0)
        self.assertTrue(os.path.isfile(full_filename))
        # test catch the wrong class
        company2 = company_from_json(self._generate_test_company(50))
        company2.class_ = "dummy"
        with self.assertRaises(AssertionError) as cm:
            storage.save(company2)
        self.assertEqual(AC_ERROR_WRONG_CLASS, cm.exception.args[0])
