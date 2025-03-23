from categories.repositories import CategoryRepository, SubCategoryRepository
from uow import BaseUnitOfWork


class CategoryUnitOfWork(BaseUnitOfWork):

    async def __aenter__(self):
        await super().__aenter__()
        self.repository = CategoryRepository(self.session)
        return self


class SubCategoryUnitOfWork(BaseUnitOfWork):

    async def __aenter__(self):
        await super().__aenter__()
        self.repository = SubCategoryRepository(self.session)
        return self
