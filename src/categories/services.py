from typing import Optional

from dependency_injector.wiring import Provide
from fastapi import HTTPException
from starlette import status

from auth.schemas import TokenUserPayload
from categories.schemas import (
    CategoryCreate,
    CategoryUpdate,
    SubCategoryCreate,
    SubCategoryUpdate,
)
from categories.uow import CategoryUnitOfWork, SubCategoryUnitOfWork
from documents.services import DocumentService
from models import Category, SubCategory


class CategoryService:

    def __init__(
        self,
        uow: CategoryUnitOfWork = Provide["category_uow"],
        sub_category_service: "SubCategoryService" = Provide["sub_category_service"],
    ):
        self.uow = uow
        self.sc_service = sub_category_service

    async def get_categories(self, page: int, size: int) -> list[Category]:
        async with self.uow:
            return await self.uow.repository.get_categories(page, size)

    async def create_category(
        self, current_user: TokenUserPayload, category_create: CategoryCreate
    ) -> Category:
        data = category_create.model_dump()
        data["parent_id"] = current_user.id
        async with self.uow:
            category = await self.uow.repository.create_category(data)
            await self.uow.commit()
            return category

    async def count_categories(self) -> int:
        async with self.uow:
            return await self.uow.repository.count_categories()

    async def update_category(self, c_id: int, c_update: CategoryUpdate) -> Category:
        async with self.uow:
            data = {k: v for k, v in c_update.model_dump().items() if v is not None}
            c = await self.uow.repository.update_category(c_id, data)
            await self.uow.commit()
            return c

    async def delete_category(self, c_id: int):
        any_sub_category = await self.sc_service.get_first_subcategory_by_category(c_id)
        if any_sub_category:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cannot delete category with ID {c_id} because it is used by at least one subcategory",
            )
        async with self.uow:
            await self.uow.repository.delete_category(c_id)
            await self.uow.commit()


class SubCategoryService:

    def __init__(
        self,
        uow: SubCategoryUnitOfWork = Provide["sub_category_uow"],
        document_service: DocumentService = Provide["document_service"],
    ):
        self.uow = uow
        self.document_service = document_service

    async def count_sub_categories(self) -> int:
        async with self.uow:
            return await self.uow.repository.count_sub_categories()

    async def get_sub_categories(self, page: int, size: int) -> list[SubCategory]:
        async with self.uow:
            return await self.uow.repository.get_sub_categories(page, size)

    async def create_sub_category(
        self, current_user: TokenUserPayload, sub_category_create: SubCategoryCreate
    ) -> SubCategory:

        data = sub_category_create.model_dump()
        data["parent_id"] = current_user.id
        async with self.uow:
            sub_category = await self.uow.repository.create_sub_category(data)
            await self.uow.commit()
            return sub_category

    async def update_sub_category(
        self, sc_id: int, sc_update: SubCategoryUpdate
    ) -> SubCategory:
        async with self.uow:
            data = {k: v for k, v in sc_update.model_dump().items() if v is not None}
            sc = await self.uow.repository.update_sub_category(sc_id, data)
            await self.uow.commit()
            return sc

    async def delete_sub_category(self, sc_id: int):
        any_document = await self.document_service.get_first_document_by_subcategory(
            sc_id
        )
        if any_document:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cannot delete sub-category with ID {sc_id} because it is used by at least one document",
            )
        async with self.uow:
            await self.uow.repository.delete_sub_category(sc_id)
            await self.uow.commit()

    async def get_first_subcategory_by_category(
        self, c_id: int
    ) -> Optional[SubCategory]:
        async with self.uow:
            return await self.uow.repository.get_first_subcategory_by_category(c_id)

    async def get_sub_categories_by_category(self, c_id: int):
        async with self.uow:
            return await self.uow.repository.get_sub_categories_by_category(c_id)
