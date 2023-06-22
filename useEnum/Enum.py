from enum import Enum


class InitializeEnum(Enum):
    STRING = "null"
    INT = 0


class SchemasEnum(Enum):
    USER = "user"
    TOKEN = "token"
    CATEGORY = "category"
    STOCK = "stocks"
    TRANSACTION = "transactions"
    SEQUENCES = "table_sequences"


class SchemaSequencesEnum(Enum):
    USER = "user_sequence"
    TOKEN = "token_sequence"
    CATEGORY = "category_sequence"
    STOCK = "stocks_sequence"
    TRANSACTION = "transactions_sequence"

class TrxSign(Enum):
    PLUS = "plus"
    MINUS = "minus"

class TrxDescriptions(Enum):
    STOCK_CREATE = "Stock created"

class Code(Enum):
    USER = 'U'
    CATEGORY = 'C'
    STOCK = 'S'
    TRANSACTION = 'T'
