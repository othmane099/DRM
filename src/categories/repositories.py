from typing import Optional

from sqlalchemy import delete, func, insert, select, update
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

    async def get_sub_categories(self, page: int, size: int) -> list[SubCategory]:
        result = await self.session.scalars(
            select(SubCategory)
            .offset((page - 1) * size)
            .limit(size)
            .order_by(SubCategory.title)
        )
        return list(result.all())

    async def create_sub_category(self, data: dict) -> Optional[SubCategory]:
        stmt = insert(SubCategory).values(**data).returning(SubCategory)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_sub_category(
        self, sc_id: int, data: dict
    ) -> Optional[SubCategory]:
        stmt = (
            update(SubCategory)
            .where(SubCategory.id == sc_id)
            .values(**data)
            .returning(SubCategory)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_sub_category(self, sc_id: int):
        await self.session.execute(delete(SubCategory).where(SubCategory.id == sc_id))

    async def count_sub_categories(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(SubCategory)
        )
        return result.scalar_one()
