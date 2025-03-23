from tags.repositories import TagRepository
from uow import BaseUnitOfWork


class TagUnitOfWork(BaseUnitOfWork):

    async def __aenter__(self):
        await super().__aenter__()
        self.repository = TagRepository(self.session)
        return self
