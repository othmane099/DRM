import bcrypt
from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException
from starlette import status

from auth.schemas import TokenUserPayload
from users.schemas import RoleCreate, RoleUpdate, UserCreate
from users.uow import PermissionUnitOfWork, RoleUnitOfWork, UserUnitOfWork
from utils.utils import cpu_bound_task


class UserService:

    @inject
    def __init__(self, uow: UserUnitOfWork = Provide["user_uow"]):
        self.uow = uow

    async def create_user(
        self, current_user: TokenUserPayload, user_create: UserCreate
    ):
        user_create.password = (
            await cpu_bound_task(
                bcrypt.hashpw, user_create.password.encode(), bcrypt.gensalt()
            )
        ).decode()
        data = user_create.model_dump()
        data["is_active"] = True
        async with self.uow:
            created_user = await self.uow.repository.create_user(data)
            await self.uow.commit()
            return created_user

    async def get_user_by_email(self, email: str):
        async with self.uow:
            user = await self.uow.repository.get_user_by_email(email)
            return user


class PermissionService:

    @inject
    def __init__(self, uow: PermissionUnitOfWork = Provide["permission_uow"]):
        self.uow = uow

    async def get_permissions(self):
        async with self.uow:
            return await self.uow.repository.get_permissions()


class RoleService:

    @inject
    def __init__(
        self,
        uow: RoleUnitOfWork = Provide["role_uow"],
        permission_service: PermissionService = Provide["permission_service"],
    ):
        self.uow = uow
        self.permission_service = permission_service

    async def create_role(self, role: RoleCreate):
        async with self.uow:
            created_role = await self.uow.repository.create_role(role)
            if role.permissions and created_role:
                all_permissions = await self.permission_service.get_permissions()
                permissions_to_add = [
                    p for p in all_permissions if p.name in role.permissions
                ]
                if permissions_to_add:
                    await self.uow.repository.add_permissions_to_role(
                        created_role.id, [p.id for p in permissions_to_add]
                    )
            await self.uow.commit()
            return created_role

    async def delete_role(self, role_id: int):
        async with self.uow:
            await self.uow.repository.delete_role(role_id)
            await self.uow.commit()

    async def update_role(self, role_id: int, role: RoleUpdate):
        async with self.uow:
            updated_role = await self.uow.repository.update_role(role_id, role)
            if updated_role is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Role not found",
                )
            if role.permissions is not None:
                all_permissions = await self.permission_service.get_permissions()
                permissions_to_add = [
                    p for p in all_permissions if p.name in role.permissions
                ]
                await self.uow.repository.remove_all_permissions_from_role(role_id)
                if permissions_to_add:
                    await self.uow.repository.add_permissions_to_role(
                        role_id, [p.id for p in permissions_to_add]
                    )
            await self.uow.commit()
            return updated_role
