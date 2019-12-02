import hashlib
from unittest import TestCase

from hmac import Hmac


class HmacTestCase(TestCase):
    def test_case_one(self):
        key = b'SecretTechno'
        message = b'Gesaffelstein - Opr'
        hmac = Hmac(key, message, hashlib.md5)
        digest = hmac.use()
        theoretical_digest = b'g\x03)9\xbefa\xbe\x80\x982\x8a\xe3.\x84x'
        print(digest)
        self.assertEqual(digest, theoretical_digest)
