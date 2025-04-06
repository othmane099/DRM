from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from starlette import status
from starlette.responses import Response

from auth import helpers
from auth.schemas import TokenUserPayload
from auth.security import get_user
from categories.schemas import (
    CategoryCreate,
    CategoryResponse,
    SCPaginationResponse,
    SubCategoryCreate,
    SubCategoryResponse,
    SubCategoryUpdate,
)
from categories.services import CategoryService, SubCategoryService
from users.permissions import (
    CAN_CREATE_CATEGORY,
    CAN_CREATE_SUB_CATEGORY,
    CAN_DELETE_SUB_CATEGORY,
    CAN_EDIT_SUB_CATEGORY,
    CAN_MANAGE_SUB_CATEGORY,
)
from utils.schemas import PaginationParams

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


@categories_router.get("/sub-categories", response_model=SCPaginationResponse)
@inject
async def get_sub_categories(
    pagination_params: Annotated[PaginationParams, Query()],
    current_user: TokenUserPayload = Depends(get_user),
    sub_category_service: SubCategoryService = Depends(Provide["sub_category_service"]),
):
    if helpers.is_authorized(current_user, CAN_MANAGE_SUB_CATEGORY):
        sub_categories = await sub_category_service.get_sub_categories(
            pagination_params.page, pagination_params.size
        )
        total = await sub_category_service.count_sub_categories()
        return SCPaginationResponse(
            total=total,
            current=pagination_params.page,
            size=pagination_params.size,
            data=sub_categories,
        )


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


@categories_router.put("/sub-categories/{sc_id}")
@inject
async def update_sub_category(
    sc_id: int,
    sc_update: SubCategoryUpdate,
    sub_category_service: SubCategoryService = Depends(Provide["sub_category_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    if helpers.is_authorized(current_user, CAN_EDIT_SUB_CATEGORY):
        return await sub_category_service.update_sub_category(sc_id, sc_update)


@categories_router.delete("/sub-categories/{sc_id}")
@inject
async def delete_sub_category(
    sc_id: int,
    sub_category_service: SubCategoryService = Depends(Provide["sub_category_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    if helpers.is_authorized(current_user, CAN_DELETE_SUB_CATEGORY):
        await sub_category_service.delete_sub_category(sc_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
