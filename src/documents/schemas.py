from typing import Optional

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    name: str
    user_id: int
    category_id: int
    sub_category_id: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
