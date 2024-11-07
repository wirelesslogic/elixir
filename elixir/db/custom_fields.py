import json
from enum import Enum
from typing import Any, Optional, Type, Union

from cryptography.exceptions import InvalidKey
from cryptography.fernet import Fernet, InvalidToken
from peewee import BlobField, SmallIntegerField, TextField


class JsonField(TextField):
    """
    A field that serializes/deserializes JSON data to/from a string.
    """

    field_type = "JSON"

    def db_value(self, value: Optional[Any]) -> Optional[str]:
        """
        Serializes Python objects to a JSON-formatted string for database storage.
        """
        if value is not None:
            try:
                return json.dumps(value, default=str)
            except TypeError as e:
                raise ValueError(f"Invalid data for JSON serialization: {e}")

    def python_value(self, value: Optional[str]) -> Optional[Any]:
        """
        Deserializes a JSON-formatted string from the database back into Python objects.
        """
        if value is not None:
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format: {e}")


class EnumField(SmallIntegerField):
    """
    A field for storing Python Enum types as integers in the database.
    """

    def __init__(self, choices: Type[Enum], *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not issubclass(choices, Enum):
            raise TypeError("Choices must be an Enum type")
        self.choices = choices
        self.valid_values = set(item.value for item in choices)

    def db_value(self, value: Union[Enum, int]) -> Optional[int]:
        """
        Converts the Enum value to its corresponding integer value for database storage.
        """
        if isinstance(value, Enum):
            return value.value
        elif isinstance(value, int):
            if value not in self.valid_values:
                raise ValueError(f"Value {value} is not a valid choice for the Enum")
            return value
        else:
            raise TypeError("Value must be an instance of the specified Enum or an int")

    def python_value(self, value: int) -> Enum:
        """
        Converts the stored integer value back to the corresponding Enum type.
        """
        return self.choices(value)


class SecureField(BlobField):
    """
    A field that encrypts data before saving to the database and decrypts data when
    retrieving from the database. It handles simple data types (str, int) directly
    and complex types (list, dict) via JSON serialization.
    """

    def __init__(self, crypto_key: str, *args, **kwargs):
        self.key = self.validate_and_return_fernet_key(crypto_key)
        super().__init__(*args, **kwargs)

    def validate_and_return_fernet_key(self, key: str):
        """
        Validates the cryptographic key and returns a Fernet object.
        """
        encoded_key = key.encode()
        try:
            return Fernet(encoded_key)
        except InvalidKey:
            raise ValueError(
                "Invalid crypto_key. Key must be 32 url-safe base64-encoded bytes."
            )

    def db_value(self, value: Optional[Any]) -> Optional[bytes]:
        """
        Encrypts the value before saving to the database.
        Complex types (list, dict) are serialized to JSON.
        """
        if value is None:
            return None

        if isinstance(value, (list, dict)):
            try:
                value = json.dumps(value, default=str)
            except TypeError as e:
                raise ValueError("Data serialization error.")

        return super().db_value(self.encrypt_data(str(value)))

    def python_value(self, value: Optional[bytes]) -> Optional[Any]:
        """
        Decrypts the database value back into Python objects.
        Attempts to deserialize JSON-formatted strings into complex types.
        """
        if value is None or value == b"":
            return None

        decrypted = self.decrypt_data(super().python_value(value))
        try:
            return json.loads(decrypted)
        except json.JSONDecodeError:
            return decrypted  # Return as string if not JSON

    def encrypt_data(self, data: str) -> bytes:
        """
        Encrypts the data using Fernet encryption.
        """
        try:
            return self.key.encrypt(data.encode("utf-8"))
        except Exception as e:
            raise ValueError(f"Encryption error: {str(e)}")

    def decrypt_data(self, data: bytes) -> str:
        """
        Decrypts the data using Fernet decryption.
        """
        try:
            return self.key.decrypt(bytes(data)).decode("utf-8")
        except (InvalidToken, TypeError) as e:
            raise ValueError(f"Decryption error: {str(e)}")
