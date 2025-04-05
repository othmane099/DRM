from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(default=0, ge=0)
    size: int = Field(default=10, ge=1)


class PaginationResponse(BaseModel):
    current: int = Field(ge=0)
    size: int = Field(ge=1)
    total: int = Field(ge=0)
    data: list
