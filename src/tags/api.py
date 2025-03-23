from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from auth import helpers
from auth.schemas import TokenUserPayload
from auth.security import get_user
from tags.schemas import TagCreate, TagResponse
from tags.services import TagService
from users.permissions import CAN_CREATE_TAG

tags_router = APIRouter(prefix="/tags", tags=["tags"])


@tags_router.post("", response_model=TagResponse)
@inject
async def create_tag(
    tag_create: TagCreate,
    tag_service: TagService = Depends(Provide["tag_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    if helpers.is_authorized(current_user, CAN_CREATE_TAG):
        return await tag_service.create_tag(current_user, tag_create)
