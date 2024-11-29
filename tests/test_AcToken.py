from unittest import TestCase

from ActiveCollabAPI.AcToken import AcToken


class TestAcToken(TestCase):
    def test_ac_token(self):
        token_str = "laksdfklajsdfkljsadlkfjakljfkl"

        token = AcToken(token=token_str)

        self.assertIsInstance(token, AcToken)
        self.assertEqual(token_str, token.token)
