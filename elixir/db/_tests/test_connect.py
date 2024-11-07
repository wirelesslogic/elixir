import hashlib
import unittest

from config import cfg
from core import log

from db import connect_to_db, main_db

secret_byte_array = bytearray()
secret_byte_array.extend(map(ord, "secret"))

incorrect_secret_byte_array = bytearray()
incorrect_secret_byte_array.extend(map(ord, "bad secret"))


class HMACTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        main_db.init(
            max_connections=32,
            stale_timeout=300,
            database="test",
            host="test",
            port=int("5432"),
            user="test",
            password="test",
        )

    @classmethod
    def tearDownClass(cls):
        if not main_db.is_closed():
            main_db.close()

    def test_connect(self):
        result = connect_to_db(main_db)

        self.assertTrue(result)
