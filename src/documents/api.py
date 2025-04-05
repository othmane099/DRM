from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, Form, UploadFile

from auth import helpers
from auth.schemas import TokenUserPayload
from auth.security import get_user
from documents.schemas import DocumentCreate, VersionHistoryCreate
from documents.services import DocumentService
from users.permissions import (
    CAN_CREATE_DOCUMENT,
    CAN_CREATE_MY_DOCUMENT,
    CAN_CREATE_VERSION,
    CAN_MANAGE_VERSION,
)

documents_router = APIRouter(prefix="/documents", tags=["documents"])


@documents_router.post("")
@inject
async def create_document(
    name: str = Form(...),
    category_id: int = Form(...),
    sub_category_id: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    tags: Optional[list[str]] = Form(None),
    file: UploadFile = File(None),
    current_user: TokenUserPayload = Depends(get_user),
    document_service: DocumentService = Depends(Provide["document_service"]),
):
    document_create = DocumentCreate(
        name=name,
        user_id=current_user.id,
        category_id=category_id,
        sub_category_id=sub_category_id,
        description=description,
        tags=tags,
    )
    if helpers.is_authorized(current_user, CAN_CREATE_DOCUMENT, CAN_CREATE_MY_DOCUMENT):
        return await document_service.create_document(
            current_user, document_create, file
        )


@documents_router.get("/{document_id}/versions")
@inject
async def get_document_versions(
    document_id: int,
    current_user: TokenUserPayload = Depends(get_user),
    document_service: DocumentService = Depends(Provide["document_service"]),
):
    if helpers.is_authorized(current_user, CAN_MANAGE_VERSION):
        return await document_service.get_document_versions(document_id)


@documents_router.post("/{document_id}/versions")
@inject
async def create_document_version(
    document_id: int,
    file: UploadFile = File(...),
    current_user: TokenUserPayload = Depends(get_user),
    document_service: DocumentService = Depends(Provide["document_service"]),
):
    if helpers.is_authorized(current_user, CAN_CREATE_VERSION):
        version_create = VersionHistoryCreate(
            document_id=document_id, created_by=current_user.id, file_name="Unknown"
        )
        return await document_service.create_document_version(version_create, file)
