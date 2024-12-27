import os
import time
from unittest import TestCase
import configparser

from active_collab_app import CFG_SECTION_DEFAULT, CFG_OPTION_DUMP_TIMESTAMP_FILE
from active_collab_app import helper


class TestHelper(TestCase):
    def test_map_user_id(self):
        config = configparser.ConfigParser(interpolation=None)
        config.set(CFG_SECTION_DEFAULT, "map_user_id_5", "1")
        user_not_mapped = helper.map_user_id(config, 10)
        self.assertEqual(10, user_not_mapped)
        self.assertIsInstance(user_not_mapped, int)
        user_is_mapped = helper.map_user_id(config, 5)
        self.assertEqual(1, user_is_mapped)
        self.assertIsInstance(user_is_mapped, int)

    def test_save_dump_timestamp_and_again_and_its_modified(self):
        config = configparser.ConfigParser(interpolation=None)
        config.set(CFG_SECTION_DEFAULT, CFG_OPTION_DUMP_TIMESTAMP_FILE, "/tmp/ts.txt")
        filename1 = helper.save_dump_timestamp(config)
        self.assertTrue(os.path.exists(filename1))
        file_stats1 = os.stat(filename1)
        time.sleep(1)
        filename2 = helper.save_dump_timestamp(config)
        self.assertTrue(os.path.exists(filename2))
        file_stats2 = os.stat(filename2)
        self.assertGreater(file_stats2.st_mtime, file_stats1.st_mtime)
