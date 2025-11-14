from typing import Optional

import bcrypt
from dependency_injector.wiring import Provide, inject

from errors import Error, ErrorType
from models import Role, User
from users.schemas import RoleCreate, RoleUpdate, UserCreate
from users.uow import PermissionUnitOfWork, RoleUnitOfWork, UserUnitOfWork
from utils.utils import cpu_bound_task


class UserService:

    @inject
    def __init__(self, uow: UserUnitOfWork = Provide["user_uow"]):
        self.uow = uow

    async def create_user(self, user_create: UserCreate) -> User | Error:
        user_create.password = (
            await cpu_bound_task(
                bcrypt.hashpw, user_create.password.encode(), bcrypt.gensalt()
            )
        ).decode()
        data = user_create.model_dump()
        data["is_active"] = True
        async with self.uow:
            result = await self.uow.repository.create_user(data)
            if isinstance(result, User):
                await self.uow.commit()
                return result
            elif result == ErrorType.UNIQUE_VIOLATION:
                return Error(
                    status_code=409,
                    message="User with email: {} already exists".format(
                        user_create.email
                    ),
                )
            else:
                return Error(status_code=500, message=str(result))

    async def update_user(self, user_id: int, user_update: UserCreate) -> User | Error:
        async with self.uow:
            result = await self.uow.repository.update_user(user_id, user_update)
            if isinstance(result, User):
                await self.uow.commit()
                return result
            elif result == ErrorType.UNIQUE_VIOLATION:
                return Error(
                    status_code=409,
                    message="User with email: {} already exists".format(
                        user_update.email
                    ),
                )
            else:
                return Error(status_code=500, message=str(result))

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

    async def get_roles(self, page: int, size: int) -> list[Role]:
        async with self.uow:
            return await self.uow.repository.get_roles(page, size)

    async def create_role(self, role: RoleCreate) -> Role | Error:
        async with self.uow:
            result = await self.uow.repository.create_role(role)
            if isinstance(result, Role):
                if role.permissions:
                    all_permissions = await self.permission_service.get_permissions()
                    permissions_to_add = [
                        p for p in all_permissions if p.name in role.permissions
                    ]
                    if permissions_to_add:
                        await self.uow.repository.add_permissions_to_role(
                            result.id, [p.id for p in permissions_to_add]
                        )
                await self.uow.commit()
                return result
            elif result == ErrorType.UNIQUE_VIOLATION:
                return Error(
                    status_code=409,
                    message="Role with name: {} already exists".format(role.name),
                )
            else:
                return Error(status_code=500, message=str(result))

    async def delete_role(self, role_id: int) -> Optional[Error]:
        async with self.uow:
            result = await self.uow.repository.delete_role(role_id)
            if result is None:
                await self.uow.commit()
                return None
            elif result == ErrorType.FOREIGN_KEY_VIOLATION:
                return Error(
                    status_code=409,
                    message="Cannot delete role because it is assigned to one or more users",
                )
            else:
                return Error(status_code=500, message=str(result))

    async def update_role(self, role_id: int, role: RoleUpdate) -> Role | Error:
        async with self.uow:
            result = await self.uow.repository.update_role(role_id, role)
            if isinstance(result, Role):
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
                return result
            elif result == ErrorType.UNIQUE_VIOLATION:
                return Error(
                    status_code=409,
                    message="Role with name: {} already exists".format(role.name),
                )
            elif result == ErrorType.ENTITY_NOT_FOUND:
                return Error(status_code=404, message="Role not found")
            else:
                return Error(status_code=500, message=str(result))

    async def count_roles(self) -> int:
        async with self.uow:
            return await self.uow.repository.count_roles()
