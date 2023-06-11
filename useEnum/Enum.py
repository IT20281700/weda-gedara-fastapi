from enum import Enum


class InitializeEnum(Enum):
    STRING = "null"
    INT = 0


class SchemasEnum(Enum):
    USER = "user"
    TOKEN = "token"
    SEQUENCES = "table_sequences"


class SchemaSequencesEnum(Enum):
    USER = "user_sequence"
    TOKEN = "token_sequence"
