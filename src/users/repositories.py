from typing import Optional

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import Permission, Role, User
from users.schemas import RoleCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, data: dict) -> Optional[User]:
        stmt = insert(User).values(**data).returning(User)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        stmt = (
            select(User)
            .where(User.email == email)
            .options(joinedload(User.role).joinedload(Role.permissions))
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_role(self, role_create: RoleCreate) -> Optional[Role]:
        stmt = (
            insert(Role)
            .values(**role_create.model_dump(exclude={"permissions"}))
            .returning(Role)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one_or_none()

    async def add_permissions_to_role(self, role_id: int, permission_ids: list[int]):
        from models import role_permission

        values = [
            {"role_id": role_id, "permission_id": permission_id}
            for permission_id in permission_ids
        ]
        if values:
            stmt = insert(role_permission).values(values)
            await self.session.execute(stmt)

    async def delete_role(self, role_id: int):
        await self.session.execute(delete(Role).where(Role.id == role_id))


class PermissionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_permissions(self):
        result = await self.session.scalars(select(Permission))
        return list(result.all())
