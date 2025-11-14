from typing import Optional

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from errors import (
    ASYNCPG_EXCEPTIONS_FOREIGN_KEY_VIOLATION,
    ASYNCPG_EXCEPTIONS_UNIQUE_VIOLATION,
    ErrorType,
)
from models import Permission, Role, User
from users.schemas import RoleCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, data: dict) -> User | ErrorType:
        stmt = insert(User).values(**data).returning(User)
        try:
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except IntegrityError as e:
            if ASYNCPG_EXCEPTIONS_UNIQUE_VIOLATION in str(
                e.orig
            ) and "users_email_key" in str(e.orig):
                return ErrorType.UNIQUE_VIOLATION
        return ErrorType.UNKNOWN_ERROR

    async def update_user(self, user_id: int, user_update: UserUpdate) -> User | ErrorType:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**user_update.model_dump())
            .returning(User)
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.flush()
            return result.scalar_one()
        except NoResultFound:
            return ErrorType.ENTITY_NOT_FOUND
        except IntegrityError as e:
            if ASYNCPG_EXCEPTIONS_UNIQUE_VIOLATION in str(
                e.orig
            ) and "users_email_key" in str(e.orig):
                return ErrorType.UNIQUE_VIOLATION
        return ErrorType.UNKNOWN_ERROR

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

    async def get_roles(self, page: int, size: int) -> list[Role]:
        result = await self.session.scalars(
            select(Role).offset((page - 1) * size).limit(size).order_by(Role.name)
        )
        return list(result.all())

    async def create_role(self, role_create: RoleCreate) -> Role | ErrorType:
        stmt = (
            insert(Role)
            .values(**role_create.model_dump(exclude={"permissions"}))
            .returning(Role)
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.flush()
            return result.scalar_one()
        except IntegrityError as e:
            if ASYNCPG_EXCEPTIONS_UNIQUE_VIOLATION in str(
                e.orig
            ) and "roles_name_key" in str(e.orig):
                return ErrorType.UNIQUE_VIOLATION
        return ErrorType.UNKNOWN_ERROR

    async def add_permissions_to_role(self, role_id: int, permission_ids: list[int]):
        from models import role_permission

        values = [
            {"role_id": role_id, "permission_id": permission_id}
            for permission_id in permission_ids
        ]
        if values:
            stmt = insert(role_permission).values(values)
            await self.session.execute(stmt)

    async def remove_all_permissions_from_role(self, role_id: int):
        from models import role_permission

        stmt = delete(role_permission).where(role_permission.c.role_id == role_id)
        await self.session.execute(stmt)
        await self.session.flush()

    async def delete_role(self, role_id: int) -> Optional[ErrorType]:
        try:
            await self.session.execute(delete(Role).where(Role.id == role_id))
            return None
        except IntegrityError as e:
            if ASYNCPG_EXCEPTIONS_FOREIGN_KEY_VIOLATION in str(
                e.orig
            ) and "users_role_id_fkey" in str(e.orig):
                return ErrorType.FOREIGN_KEY_VIOLATION
        return ErrorType.UNKNOWN_ERROR

    async def update_role(
        self, role_id: int, role_update: RoleCreate
    ) -> Role | ErrorType:
        stmt = (
            update(Role)
            .where(Role.id == role_id)
            .values(**role_update.model_dump(exclude={"permissions"}))
            .returning(Role)
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.flush()
            return result.scalar_one()
        except NoResultFound:
            return ErrorType.ENTITY_NOT_FOUND
        except IntegrityError as e:
            if ASYNCPG_EXCEPTIONS_UNIQUE_VIOLATION in str(
                e.orig
            ) and "roles_name_key" in str(e.orig):
                return ErrorType.UNIQUE_VIOLATION
        return ErrorType.UNKNOWN_ERROR

    async def count_roles(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(Role))
        return result.scalar_one()


class PermissionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_permissions(self):
        result = await self.session.scalars(select(Permission))
        return list(result.all())
