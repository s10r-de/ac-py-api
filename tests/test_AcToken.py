from unittest import TestCase

from active_collab_api.ac_token import AcToken


class TestAcToken(TestCase):
    def test_ac_token(self):
        # noinspection SpellCheckingInspection
        token_str = "laksdfklajsdfkljsadlkfjakljfkl"

        token = AcToken(token=token_str)

        self.assertIsInstance(token, AcToken)
        self.assertEqual(token_str, token.token)
