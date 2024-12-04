import json
from unittest import TestCase

from active_collab_api import AC_PROPERTY_CLASS, AC_PROPERTY_CLASS_
from active_collab_api.ac_user import (
    AC_CLOUD_LANG_ID_ENGLISH,
    AC_CLOUD_LANG_ID_GERMAN,
    AC_SELFHOSTED_LANG_ID_ENGLISH,
    AC_SELFHOSTED_LANG_ID_GERMAN,
    generate_random_password,
    map_cloud_user_language_id,
    user_from_json,
)


class TestAcUser(TestCase):
    @staticmethod
    def _generate_test_user(user_id: int) -> dict:
        with open(
            "tests/example-data/example-user-00000240.json", "r", encoding="utf-8"
        ) as fh:
            user_json = json.load(fh)
        user_json["id"] = user_id
        return user_json

    def test_to_dict(self):
        user_id = 100
        user_json = self._generate_test_user(user_id)
        user = user_from_json(user_json)
        user_dict = user.to_dict()
        self.assertEqual(user_id, user_dict["id"])
        self.assertIn(AC_PROPERTY_CLASS, user_dict.keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, user_dict.keys())

    def test_to_json(self):
        user_id = 102
        user_json = self._generate_test_user(user_id)
        user = user_from_json(user_json)
        user_json = user.to_json()
        self.assertEqual(user_id, json.loads(user_json)["id"])
        self.assertIn(AC_PROPERTY_CLASS, json.loads(user_json).keys())
        self.assertNotIn(AC_PROPERTY_CLASS_, json.loads(user_json).keys())

    def test_map_cloud_user_language_id_de(self):
        user_id = 103
        cloud_user_de_json = self._generate_test_user(user_id)
        cloud_user_de = user_from_json(cloud_user_de_json)
        cloud_user_de.language_id = AC_CLOUD_LANG_ID_GERMAN
        self_hosted_user_de = map_cloud_user_language_id(cloud_user_de)
        self.assertEqual(self_hosted_user_de.language_id, AC_SELFHOSTED_LANG_ID_GERMAN)

    def test_map_cloud_user_language_id_en(self):
        user_id = 103
        cloud_user_de_json = self._generate_test_user(user_id)
        cloud_user_de = user_from_json(cloud_user_de_json)
        cloud_user_de.language_id = AC_CLOUD_LANG_ID_ENGLISH
        self_hosted_user_de = map_cloud_user_language_id(cloud_user_de)
        self.assertEqual(self_hosted_user_de.language_id, AC_SELFHOSTED_LANG_ID_ENGLISH)

    def test_map_cloud_user_language_id_other(self):
        user_id = 103
        cloud_user_de_json = self._generate_test_user(user_id)
        cloud_user_de = user_from_json(cloud_user_de_json)
        cloud_user_de.language_id = 18  # some random value not DE not EN
        self_hosted_user_de = map_cloud_user_language_id(cloud_user_de)
        self.assertEqual(self_hosted_user_de.language_id, AC_SELFHOSTED_LANG_ID_ENGLISH)

    def test_generate_random_password(self):
        user_id = 103
        user_json = self._generate_test_user(user_id)
        user = user_from_json(user_json)
        password0 = user.password
        user = generate_random_password(user)
        password1 = user.password
        self.assertNotEqual(password0, password1)
        user = generate_random_password(user)
        password2 = user.password
        self.assertNotEqual(password0, password2)
        self.assertNotEqual(password1, password2)
