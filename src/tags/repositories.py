from typing import Optional

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Tag


class TagRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tags(self, page: int, size: int) -> list[Tag]:
        result = await self.session.scalars(
            select(Tag).offset((page - 1) * size).limit(size).order_by(Tag.title)
        )
        return list(result.all())

    async def create_tag(self, data: dict) -> Optional[Tag]:
        stmt = insert(Tag).values(**data).returning(Tag)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_tag(self, tag_id: int, data: dict) -> Optional[Tag]:
        stmt = update(Tag).where(Tag.id == tag_id).values(**data).returning(Tag)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_tag(self, tag_id: int):
        await self.session.execute(delete(Tag).where(Tag.id == tag_id))

    async def count_tags(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(Tag))
        return result.scalar_one()
