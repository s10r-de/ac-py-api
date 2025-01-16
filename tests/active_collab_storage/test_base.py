import copy
import inspect
import json
import os.path
import random
import shutil
from unittest import TestCase

from active_collab_api.ac_company import company_from_json
from active_collab_storage.base import AcFileStorageBaseClass

DATA_DIR = "./data-test/TestAcFileStorageBaseClass/"
ACCOUNT_ID = 98765

TEST_FILENAME_PREFIX = "test-file-prefix"
TEST_DIR_NAME = "test-dir"


class TestBase(TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.exists(DATA_DIR):
            rand = random.random()
            tmp = DATA_DIR.rstrip("/") + f"{rand:#0.6f}"
            os.rename(DATA_DIR, tmp)
            shutil.rmtree(tmp)

    def test_reset(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID)
        storage.filename_prefix = TEST_FILENAME_PREFIX
        storage.dir_name = TEST_DIR_NAME
        storage.reset()
        filename = storage.get_path()
        self.assertFalse(os.path.isdir(filename))

    def test_ensure_dirs(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID)
        storage.filename_prefix = TEST_FILENAME_PREFIX
        storage.dir_name = TEST_DIR_NAME
        storage.ensure_dirs()
        filename = storage.get_path()
        self.assertTrue(os.path.isdir(filename))

    def test_get_account_path(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID)
        storage.filename_prefix = TEST_FILENAME_PREFIX
        storage.dir_name = TEST_DIR_NAME
        filename = storage.get_account_path()
        self.assertGreater(len(filename), 0)
        regex_ac = r"%s/account-%08d" % (DATA_DIR + m_name, ACCOUNT_ID)
        self.assertRegex(filename, regex_ac)

    def test_get_path(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID)
        storage.filename_prefix = TEST_FILENAME_PREFIX
        storage.dir_name = TEST_DIR_NAME
        path = storage.get_path()
        self.assertGreater(len(path), 0)
        self.assertRegex(path, TEST_DIR_NAME)

    def test_filename_with_id(self):
        m_name = inspect.stack()[0][3]
        test_id = 888
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID)
        storage.filename_prefix = TEST_FILENAME_PREFIX
        storage.dir_name = TEST_DIR_NAME
        filename = storage.filename_with_id(test_id)
        self.assertGreater(len(filename), 0)
        regex = r".*-%018d.json$" % test_id
        self.assertRegex(filename, regex)

    def test_get_full_filename(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID)
        storage.filename_prefix = TEST_FILENAME_PREFIX
        storage.dir_name = TEST_DIR_NAME
        filename = storage.get_full_filename(TEST_FILENAME_PREFIX)
        self.assertGreater(len(filename), 0)
        regex = r".*/%s$" % TEST_FILENAME_PREFIX
        self.assertRegex(filename, regex)
        regex_ac = r"%s/account-%08d/%s/%s" % (
            DATA_DIR + m_name,
            ACCOUNT_ID,
            TEST_DIR_NAME,
            TEST_FILENAME_PREFIX,
        )
        self.assertRegex(filename, regex_ac)

    def test_save_with_id(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID)
        storage.filename_prefix = TEST_FILENAME_PREFIX
        storage.dir_name = TEST_DIR_NAME
        storage.reset()
        storage.ensure_dirs()
        with open(
            "tests/example-data/example-company-5.json", "r", encoding="utf-8"
        ) as fh:
            company_json = json.load(fh)
            company = company_from_json(company_json)
        filename = storage.save_with_id(company, company.id)
        self.assertGreater(len(filename), 0)
        regex = r".*-%018d.json$" % company.id
        self.assertRegex(filename, regex)
        self.assertTrue(os.path.exists(filename))

    def test_list_is_empty(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID)
        storage.filename_prefix = TEST_FILENAME_PREFIX
        storage.dir_name = TEST_DIR_NAME
        storage.reset()
        storage.ensure_dirs()
        ids = storage.list_ids()
        with self.assertRaises(StopIteration):
            next(ids)

    def test_list_has_two_items(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID)
        storage.filename_prefix = TEST_FILENAME_PREFIX
        storage.dir_name = TEST_DIR_NAME
        storage.reset()
        storage.ensure_dirs()
        with open(
            "tests/example-data/example-company-5.json", "r", encoding="utf-8"
        ) as fh:
            company_json = json.load(fh)
            company = company_from_json(company_json)
        company77 = copy.copy(company)
        company77.id = 77
        company88 = copy.copy(company)
        company88.id = 88
        company123 = copy.copy(company)
        company123.id = 123
        storage.save_with_id(company123, company123.id)
        storage.save_with_id(company88, company88.id)
        storage.save_with_id(company77, company77.id)
        ids = storage.list_ids()  # must be sorted
        item_id = next(ids)
        self.assertEqual(77, item_id)
        item_id = next(ids)
        self.assertEqual(88, item_id)
        item_id = next(ids)
        self.assertEqual(123, item_id)
        with self.assertRaises(StopIteration):
            next(ids)

    def test_load(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID)
        storage.filename_prefix = TEST_FILENAME_PREFIX
        storage.dir_name = TEST_DIR_NAME
        storage.reset()
        storage.ensure_dirs()
        with open(
            "tests/example-data/example-company-5.json", "r", encoding="utf-8"
        ) as fh:
            company_json = json.load(fh)
            company = company_from_json(company_json)
        company.id = 44
        storage.save_with_id(company, company.id)
        loaded_comp = storage.load_by_id(44)
        self.assertEqual(company.class_, loaded_comp["class"])
        self.assertEqual(company.id, loaded_comp["id"])
        self.assertEqual(company.name, loaded_comp["name"])

    def test_get_all_two_items(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID)
        storage.filename_prefix = TEST_FILENAME_PREFIX
        storage.dir_name = TEST_DIR_NAME
        storage.reset()
        storage.ensure_dirs()
        with open(
            "tests/example-data/example-company-5.json", "r", encoding="utf-8"
        ) as fh:
            company_json = json.load(fh)
            company = company_from_json(company_json)
        company77 = copy.copy(company)
        company77.id = 77
        company88 = copy.copy(company)
        company88.id = 88

        storage.save_with_id(company88, company88.id)
        storage.save_with_id(company77, company77.id)

        all_items = storage.get_all()
        item = next(all_items)
        self.assertEqual(company77.id, item["id"])
        item = next(all_items)
        self.assertEqual(company88.id, item["id"])
        with self.assertRaises(StopIteration):
            next(all_items)
