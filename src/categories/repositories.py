from typing import Optional

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Category, SubCategory


class CategoryRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, data: dict) -> Optional[Category]:
        stmt = insert(Category).values(**data).returning(Category)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class SubCategoryRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_sub_category(self, data: dict) -> Optional[SubCategory]:
        stmt = insert(SubCategory).values(**data).returning(SubCategory)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
