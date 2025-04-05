from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.params import Query

from auth import helpers
from auth.schemas import TokenUserPayload
from auth.security import get_user
from tags.schemas import TagCreate, TagPaginationResponse, TagResponse, TagUpdate
from tags.services import TagService
from users.permissions import (
    CAN_CREATE_TAG,
    CAN_DELETE_TAG,
    CAN_EDIT_TAG,
    CAN_MANAGE_TAG,
)
from utils.schemas import PaginationParams

tags_router = APIRouter(prefix="/tags", tags=["tags"])


@tags_router.get("", response_model=TagPaginationResponse)
@inject
async def get_tags(
    pagination_params: Annotated[PaginationParams, Query()],
    tag_service: TagService = Depends(Provide["tag_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    if helpers.is_authorized(current_user, CAN_MANAGE_TAG):
        tags = await tag_service.get_tags(
            pagination_params.page, pagination_params.size
        )
        total = await tag_service.count_tags()
        return TagPaginationResponse(
            total=total,
            current=pagination_params.page,
            size=pagination_params.size,
            data=tags,
        )


@tags_router.post("", response_model=TagResponse)
@inject
async def create_tag(
    tag_create: TagCreate,
    tag_service: TagService = Depends(Provide["tag_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    if helpers.is_authorized(current_user, CAN_CREATE_TAG):
        return await tag_service.create_tag(current_user, tag_create)


@tags_router.put("/{tag_id}")
@inject
async def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    tag_service: TagService = Depends(Provide["tag_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    if helpers.is_authorized(current_user, CAN_EDIT_TAG):
        return await tag_service.update_tag(tag_id, tag_update)


@tags_router.delete("/{tag_id}")
@inject
async def delete_tag(
    tag_id: int,
    tag_service: TagService = Depends(Provide["tag_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    if helpers.is_authorized(current_user, CAN_DELETE_TAG):
        return await tag_service.delete_tag(tag_id)
