from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from utils.schemas import PaginationResponse


class TagCreate(BaseModel):
    title: str


class TagUpdate(BaseModel):
    title: Optional[str] = None


class TagResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class TagPaginationResponse(PaginationResponse):
    data: list[TagResponse]
