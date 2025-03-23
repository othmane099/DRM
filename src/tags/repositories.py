from typing import Optional

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Tag


class TagRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_tag(self, data: dict) -> Optional[Tag]:
        stmt = insert(Tag).values(**data).returning(Tag)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
