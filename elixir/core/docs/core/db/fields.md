Module core.db.fields
=====================

Classes
-------

`EnumField(choices: Type[enum.Enum], *args, **kwargs)`
:   A field for storing Python Enum types as integers in the database.

    ### Ancestors (in MRO)

    * peewee.SmallIntegerField
    * peewee.IntegerField
    * peewee.Field
    * peewee.ColumnBase
    * peewee.Node

    ### Methods

    `db_value(self, value: Union[enum.Enum, int]) ‑> Optional[int]`
    :   Converts the Enum value to its corresponding integer value for database storage.

    `python_value(self, value: int) ‑> enum.Enum`
    :   Converts the stored integer value back to the corresponding Enum type.

`JsonField(null=False, index=False, unique=False, column_name=None, default=None, primary_key=False, constraints=None, sequence=None, collation=None, unindexed=False, choices=None, help_text=None, verbose_name=None, index_type=None, db_column=None)`
:   A field that serializes/deserializes JSON data to/from a string.

    ### Ancestors (in MRO)

    * peewee.TextField
    * peewee._StringField
    * peewee.Field
    * peewee.ColumnBase
    * peewee.Node

    ### Class variables

    `field_type`
    :

    ### Methods

    `db_value(self, value: Optional[Any]) ‑> Optional[str]`
    :   Serializes Python objects to a JSON-formatted string for database storage.

    `python_value(self, value: Optional[str]) ‑> Optional[Any]`
    :   Deserializes a JSON-formatted string from the database back into Python objects.

`SecureField(crypto_key: str, *args, **kwargs)`
:   A field that encrypts data before saving to the database and decrypts data when
    retrieving from the database. It handles simple data types (str, int) directly
    and complex types (list, dict) via JSON serialization.

    ### Ancestors (in MRO)

    * peewee.BlobField
    * peewee.Field
    * peewee.ColumnBase
    * peewee.Node

    ### Static methods

    `validate_and_return_fernet_key(key: str)`
    :   Validates the cryptographic key and returns a Fernet object.

    ### Methods

    `db_value(self, value: Optional[Any]) ‑> Optional[bytes]`
    :   Encrypts the value before saving to the database.
        Complex types (list, dict) are serialized to JSON.

    `decrypt_data(self, data: bytes) ‑> str`
    :   Decrypts the data using Fernet decryption.

    `encrypt_data(self, data: str) ‑> bytes`
    :   Encrypts the data using Fernet encryption.

    `python_value(self, value: Optional[bytes]) ‑> Optional[Any]`
    :   Decrypts the database value back into Python objects.
        Attempts to deserialize JSON-formatted strings into complex types.