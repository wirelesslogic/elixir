import hashlib
import unittest

from ..auth import AuthenticationMethodHmac

secret_byte_array = bytearray()
secret_byte_array.extend(map(ord, "secret"))

incorrect_secret_byte_array = bytearray()
incorrect_secret_byte_array.extend(map(ord, "bad secret"))


class HMACTestCase(unittest.TestCase):
    # When handle_key is implemented and the test is not updated it will work as a reminder to properly test!
    def test_handle_key(self):
        status, message = AuthenticationMethodHmac.handle_key("")

        self.assertEqual(status, False)
        self.assertEqual(message, "Not implemented")

    def test_create_basic_signature(self):
        main_signature = AuthenticationMethodHmac.create_signature(
            secret_byte_array, "this key works!".encode("ascii")
        )

        correct_signature = AuthenticationMethodHmac.create_signature(
            secret_byte_array, "this key works!".encode("ascii")
        )
        incorrect_signature = AuthenticationMethodHmac.create_signature(
            secret_byte_array, "this key works?".encode("ascii")
        )
        incorrect_signature_2 = AuthenticationMethodHmac.create_signature(
            incorrect_secret_byte_array, "this key works!".encode("ascii")
        )

        self.assertEqual(main_signature, correct_signature)
        self.assertNotEqual(main_signature, incorrect_signature)
        self.assertNotEqual(main_signature, incorrect_signature_2)

    def test_create_signature_algorithms(self):
        main_signature = AuthenticationMethodHmac.create_signature(
            secret_byte_array, "this key works!".encode("ascii"), algorithm=hashlib.sha1
        )

        correct_signature = AuthenticationMethodHmac.create_signature(
            secret_byte_array, "this key works!".encode("ascii"), algorithm=hashlib.sha1
        )
        incorrect_signature = AuthenticationMethodHmac.create_signature(
            secret_byte_array,
            "this key works!".encode("ascii"),
            algorithm=hashlib.sha256,
        )

        self.assertEqual(main_signature, correct_signature)
        self.assertNotEqual(main_signature, incorrect_signature)

    def test_validate_signature(self):
        signature = AuthenticationMethodHmac.create_signature(
            secret_byte_array, "this key works!".encode("ascii")
        )

        success = AuthenticationMethodHmac.validate_incoming_signature(
            signature, secret_byte_array, "this key works!".encode("ascii")
        )
        failure = AuthenticationMethodHmac.validate_incoming_signature(
            signature, secret_byte_array, "this key works?".encode("ascii")
        )

        self.assertEqual(success, True)
        self.assertEqual(failure, False)

    def test_create_str_signature(self):
        main_signature = AuthenticationMethodHmac.create_signature(
            "secret", "this key works!"
        )

        correct_signature = AuthenticationMethodHmac.create_signature(
            secret_byte_array, "this key works!".encode("ascii")
        )

        self.assertEqual(main_signature, correct_signature)

    def test_validate_signature_from_strs(self):
        signature = AuthenticationMethodHmac.create_signature(
            "secret", "this key works!"
        )

        success = AuthenticationMethodHmac.validate_incoming_signature(
            signature, secret_byte_array, "this key works!".encode("ascii")
        )
        str_success = AuthenticationMethodHmac.validate_incoming_signature(
            signature, "secret", "this key works!"
        )
        failure = AuthenticationMethodHmac.validate_incoming_signature(
            signature, secret_byte_array, "this key works?".encode("ascii")
        )

        self.assertEqual(success, True)
        self.assertEqual(str_success, True)
        self.assertEqual(failure, False)
