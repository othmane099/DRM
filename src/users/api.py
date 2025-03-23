from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from auth import helpers
from auth.schemas import TokenUserPayload
from auth.security import get_user
from users.permissions import CAN_CREATE_USER
from users.schemas import RoleCreate, UserCreate, UserResponse
from users.services import PermissionService, RoleService, UserService

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


@users_router.get("/permissions")
@inject
async def get_permissions(
    permission_service: PermissionService = Depends(Provide["permission_service"]),
):
    return await permission_service.get_permissions()


@users_router.post("/roles")
@inject
async def create_role(
    role_create: RoleCreate,
    role_service: RoleService = Depends(Provide["role_service"]),
):
    return await role_service.create_role(role_create)
