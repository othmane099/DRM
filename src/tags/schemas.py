from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TagCreate(BaseModel):
    title: str


class TagResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
