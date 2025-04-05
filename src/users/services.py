import bcrypt
from dependency_injector.wiring import Provide, inject

from auth.schemas import TokenUserPayload
from users.schemas import RoleCreate, UserCreate
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
        data["parent_id"] = current_user.id
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
