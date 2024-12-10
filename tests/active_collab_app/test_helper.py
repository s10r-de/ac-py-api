from unittest import TestCase
import configparser

from active_collab_app.helper import map_user_id


class TestHelper(TestCase):

    def test_map_user_id(self):
        config = configparser.ConfigParser(interpolation=None)
        config.set("DEFAULT", "map_user_id_5", "1")
        user_not_mapped = map_user_id(config, 10)
        self.assertEqual(10, user_not_mapped)
        self.assertIsInstance(user_not_mapped, int)
        user_is_mapped = map_user_id(config, 5)
        self.assertEqual(1, user_is_mapped)
        self.assertIsInstance(user_is_mapped, int)
