from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from auth import helpers
from auth.schemas import TokenUserPayload
from auth.security import get_user
from categories.schemas import (
    CategoryCreate,
    CategoryResponse,
    SubCategoryCreate,
    SubCategoryResponse,
)
from categories.services import CategoryService, SubCategoryService
from users.permissions import CAN_CREATE_CATEGORY, CAN_CREATE_SUB_CATEGORY

categories_router = APIRouter(prefix="/categories", tags=["categories"])


@categories_router.post("", response_model=CategoryResponse)
@inject
async def create_category(
    category_create: CategoryCreate,
    category_service: CategoryService = Depends(Provide["category_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    if helpers.is_authorized(current_user, CAN_CREATE_CATEGORY):
        return await category_service.create_category(current_user, category_create)


@categories_router.post("/sub-categories", response_model=SubCategoryResponse)
@inject
async def create_sub_category(
    sub_category_create: SubCategoryCreate,
    sub_category_service: SubCategoryService = Depends(Provide["sub_category_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    if helpers.is_authorized(current_user, CAN_CREATE_SUB_CATEGORY):
        return await sub_category_service.create_sub_category(
            current_user, sub_category_create
        )
