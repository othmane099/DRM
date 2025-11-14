from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
from starlette.responses import Response

from auth import helpers
from auth.schemas import TokenUserPayload
from auth.security import get_user
from models import Role, User
from users.permissions import CAN_CREATE_USER, CAN_EDIT_USER
from users.schemas import (
    RoleCreate,
    RolePaginationResponse,
    RoleUpdate,
    UserCreate,
    UserResponse, UserUpdate,
)
from users.services import PermissionService, RoleService, UserService
from utils.schemas import PaginationParams

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("", response_model=UserResponse)
@inject
async def create_user(
    user_create: UserCreate,
    user_service: UserService = Depends(Provide["user_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    helpers.is_authorized(current_user, CAN_CREATE_USER)
    result = await user_service.create_user(user_create)
    try:
        assert isinstance(result, User)
        return result
    except AssertionError:
        raise HTTPException(status_code=result.status_code, detail=result.message)


@users_router.put("/{user_id}", response_model=UserResponse)
@inject
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_service: UserService = Depends(Provide["user_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    helpers.is_authorized(current_user, CAN_EDIT_USER)
    result = await user_service.update_user(user_id, user_update)
    try:
        assert isinstance(result, User)
        return result
    except AssertionError:
        raise HTTPException(status_code=result.status_code, detail=result.message)


@users_router.get("/permissions")
@inject
async def get_permissions(
    permission_service: PermissionService = Depends(Provide["permission_service"]),
):
    return await permission_service.get_permissions()


@users_router.get("/roles")
@inject
async def get_roles(
    pagination_params: Annotated[PaginationParams, Query()],
    current_user: TokenUserPayload = Depends(get_user),
    role_service: RoleService = Depends(Provide["role_service"]),
):
    if helpers.is_authorized(current_user, None):
        roles = await role_service.get_roles(
            pagination_params.page, pagination_params.size
        )
        total = await role_service.count_roles()
        return RolePaginationResponse(
            total=total,
            current=pagination_params.page,
            size=pagination_params.size,
            data=roles,
        )
    return None


@users_router.post("/roles")
@inject
async def create_role(
    role_create: RoleCreate,
    role_service: RoleService = Depends(Provide["role_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    helpers.is_authorized(current_user, None)
    result = await role_service.create_role(role_create)
    try:
        assert isinstance(result, Role)
        return result
    except AssertionError:
        raise HTTPException(status_code=result.status_code, detail=result.message)


@users_router.delete("/roles/{role_id}")
@inject
async def delete_role(
    role_id: int,
    role_service: RoleService = Depends(Provide["role_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    helpers.is_authorized(current_user, None)
    result = await role_service.delete_role(role_id)
    try:
        assert result is None
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except AssertionError:
        raise HTTPException(status_code=result.status_code, detail=result.message)


@users_router.put("/roles/{role_id}")
@inject
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    role_service: RoleService = Depends(Provide["role_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    helpers.is_authorized(current_user, None)
    result = await role_service.update_role(role_id, role_update)
    try:
        assert isinstance(result, Role)
        return result
    except AssertionError:
        raise HTTPException(status_code=result.status_code, detail=result.message)
