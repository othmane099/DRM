from documents.repositories import DocumentRepository
from uow import BaseUnitOfWork


class DocumentUnitOfWork(BaseUnitOfWork):

    async def __aenter__(self):
        await super().__aenter__()
        self.repository = DocumentRepository(self.session)
        return self

    async def flush(self):
        await self.session.flush()
