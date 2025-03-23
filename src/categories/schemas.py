from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    title: str


class CategoryResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class SubCategoryCreate(BaseModel):
    category_id: int
    title: str


class SubCategoryResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
