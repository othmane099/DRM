import dataclasses
from enum import Enum
from typing import Final

ASYNCPG_EXCEPTIONS_UNIQUE_VIOLATION: Final[str] = (
    "asyncpg.exceptions.UniqueViolationError"
)
ASYNCPG_EXCEPTIONS_FOREIGN_KEY_VIOLATION: Final[str] = (
    "asyncpg.exceptions.ForeignKeyViolationError"
)


class ErrorType(Enum):
    ENTITY_NOT_FOUND = "ENTITY_NOT_FOUND"
    UNIQUE_VIOLATION = "UNIQUE_VIOLATION"
    FOREIGN_KEY_VIOLATION = "FOREIGN_KEY_VIOLATION"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


@dataclasses.dataclass
class Error:
    status_code: int
    message: str
