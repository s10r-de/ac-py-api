import copy
import inspect
import json
import os.path
import shutil
from unittest import TestCase

from AcCompany import company_from_json
from AcFileStorageBaseClass import AcFileStorageBaseClass

DATA_DIR = './data-test/TestAcFileStorageBaseClass/'
ACCOUNT_ID = 98765

TEST_FILENAME_PREFIX = "test-file-prefix"
TEST_DIR_NAME = "test-dir"


class TestAcFileStorageBaseClass(TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(DATA_DIR):
            tmp = DATA_DIR.rstrip("/") + ".tmp"
            os.rename(DATA_DIR, tmp)
            shutil.rmtree(tmp)

    def test_reset(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID, TEST_FILENAME_PREFIX, TEST_DIR_NAME)
        storage.reset()
        filename = storage.get_path()
        self.assertFalse(os.path.isdir(filename))

    def test_ensure_dirs(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID, TEST_FILENAME_PREFIX, TEST_DIR_NAME)
        storage.ensure_dirs()
        filename = storage.get_path()
        self.assertTrue(os.path.isdir(filename))

    def test_get_account_path(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID, TEST_FILENAME_PREFIX, TEST_DIR_NAME)
        filename = storage.get_account_path()
        self.assertGreater(len(filename), 0)
        regex_ac = r'%s/account-%08d' % (DATA_DIR + m_name, ACCOUNT_ID)
        self.assertRegex(filename, regex_ac)

    def test_get_path(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID, TEST_FILENAME_PREFIX, TEST_DIR_NAME)
        path = storage.get_path()
        self.assertGreater(len(path), 0)
        self.assertRegex(path, TEST_DIR_NAME)

    def test_get_filename_id_from_object(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID, TEST_FILENAME_PREFIX, TEST_DIR_NAME)
        with open('../example-data/example-company-5.json', 'r') as fh:
            company_json = json.load(fh)
            company = company_from_json(company_json)
        filename = storage.get_filename(company)
        self.assertGreater(len(filename), 0)
        regex = r'.*-%08d.json$' % (company.id)
        self.assertRegex(filename, regex)

    def test_filename_with_id(self):
        m_name = inspect.stack()[0][3]
        test_id = 888
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID, TEST_FILENAME_PREFIX, TEST_DIR_NAME)
        filename = storage.filename_with_id(test_id)
        self.assertGreater(len(filename), 0)
        regex = r'.*-%08d.json$' % test_id
        self.assertRegex(filename, regex)

    def test_get_full_filename(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID, TEST_FILENAME_PREFIX, TEST_DIR_NAME)
        filename = storage.get_full_filename(TEST_FILENAME_PREFIX)
        self.assertGreater(len(filename), 0)
        regex = r'.*/%s$' % (TEST_FILENAME_PREFIX)
        self.assertRegex(filename, regex)
        regex_ac = r'%s/account-%08d/%s/%s' % (DATA_DIR + m_name, ACCOUNT_ID, TEST_DIR_NAME, TEST_FILENAME_PREFIX)
        self.assertRegex(filename, regex_ac)

    def test_save(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID, TEST_FILENAME_PREFIX, TEST_DIR_NAME)
        storage.reset()
        storage.ensure_dirs()
        with open('../example-data/example-company-5.json', 'r') as fh:
            company_json = json.load(fh)
            company = company_from_json(company_json)
        filename = storage.save(company)
        self.assertGreater(len(filename), 0)
        regex = r'.*-%08d.json$' % (company.id)
        self.assertRegex(filename, regex)
        self.assertTrue(os.path.exists(filename))

    def test_list(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID, TEST_FILENAME_PREFIX, TEST_DIR_NAME)
        storage.reset()
        storage.ensure_dirs()
        with open('../example-data/example-company-5.json', 'r') as fh:
            company_json = json.load(fh)
            company = company_from_json(company_json)
        company77 = copy.copy(company)
        company77.id = 77
        storage.save(company77)
        company88 = copy.copy(company)
        company88.id = 88
        storage.save(company88)
        items = storage.list()
        self.assertIn(77, items)
        self.assertIn(88, items)
        self.assertEqual(2, len(items))

    def test_load(self):
        m_name = inspect.stack()[0][3]
        storage = AcFileStorageBaseClass(DATA_DIR + m_name, ACCOUNT_ID, TEST_FILENAME_PREFIX, TEST_DIR_NAME)
        storage.reset()
        storage.ensure_dirs()
        with open('../example-data/example-company-5.json', 'r') as fh:
            company_json = json.load(fh)
            company = company_from_json(company_json)
        company.id = 44
        storage.save(company)
        loaded_comp = storage.load(44)
        self.assertEqual(company.class_, loaded_comp["class"])
        self.assertEqual(company.id, loaded_comp["id"])
        self.assertEqual(company.name, loaded_comp["name"])
