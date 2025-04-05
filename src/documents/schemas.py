from typing import Optional

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    name: str
    user_id: int
    category_id: int
    sub_category_id: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None


class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    sub_category_id: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None


class VersionHistoryCreate(BaseModel):
    document_id: int
    created_by: int
    current_version: bool = True
    document_name: str


class DocumentHistoryCreate(BaseModel):
    document_id: int
    action_by: int
    action: Optional[str] = None
    description: Optional[str] = None
