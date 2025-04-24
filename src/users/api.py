from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from starlette import status

from auth import helpers
from auth.schemas import TokenUserPayload
from auth.security import get_user
from users.permissions import CAN_CREATE_USER
from users.schemas import (
    RoleCreate,
    RolePaginationResponse,
    RoleUpdate,
    UserCreate,
    UserResponse,
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
    if helpers.is_authorized(current_user, CAN_CREATE_USER):
        return await user_service.create_user(current_user, user_create)
    return None


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
    if helpers.is_authorized(current_user, None):
        try:
            return await role_service.create_role(role_create)
        except IntegrityError as e:
            if "asyncpg.exceptions.UniqueViolationError" in str(
                e.orig
            ) and "roles_name_key" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Role name already exists.",
                )
    return None


@users_router.delete("/roles/{role_id}")
@inject
async def delete_role(
    role_id: int,
    role_service: RoleService = Depends(Provide["role_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):
    if helpers.is_authorized(current_user, None):
        try:
            return await role_service.delete_role(role_id)
        except IntegrityError as e:
            if "asyncpg.exceptions.ForeignKeyViolationError" in str(
                e.orig
            ) and "users_role_id_fkey" in str(e.orig):
                raise HTTPException(
                    status_code=409,
                    detail="Cannot delete role because it is assigned to one or more users.",
                )
    return None


@users_router.put("/roles/{role_id}")
@inject
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    role_service: RoleService = Depends(Provide["role_service"]),
    current_user: TokenUserPayload = Depends(get_user),
):

    if helpers.is_authorized(current_user, None):
        try:
            return await role_service.update_role(role_id, role_update)
        except IntegrityError as e:
            if "asyncpg.exceptions.UniqueViolationError" in str(
                e.orig
            ) and "roles_name_key" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Role name already exists.",
                )
    return None
