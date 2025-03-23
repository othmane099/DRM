from dependency_injector.wiring import Provide

from auth.schemas import TokenUserPayload
from categories.schemas import CategoryCreate, SubCategoryCreate
from categories.uow import CategoryUnitOfWork, SubCategoryUnitOfWork
from models import Category, SubCategory


class CategoryService:

    def __init__(self, uow: CategoryUnitOfWork = Provide["category_uow"]):
        self.uow = uow

    async def create_category(
        self, current_user: TokenUserPayload, category_create: CategoryCreate
    ) -> Category:
        data = category_create.model_dump()
        data["parent_id"] = current_user.id
        async with self.uow:
            category = await self.uow.repository.create_category(data)
            await self.uow.commit()
            return category


class SubCategoryService:

    def __init__(self, uow: SubCategoryUnitOfWork = Provide["sub_category_uow"]):
        self.uow = uow

    async def create_sub_category(
        self, current_user: TokenUserPayload, sub_category_create: SubCategoryCreate
    ) -> SubCategory:

        data = sub_category_create.model_dump()
        data["parent_id"] = current_user.id
        async with self.uow:
            sub_category = await self.uow.repository.create_sub_category(data)
            await self.uow.commit()
            return sub_category
