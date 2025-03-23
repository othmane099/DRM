from typing import Final

DATABASE_URL: Final[str] = (
    "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
)
JWT_SECRET: Final[str] = "secret"
JWT_ALGORITHM: Final[str] = "HS256"
