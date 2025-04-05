from documents.repositories import (
    DocumentHistoryRepository,
    DocumentRepository,
    VersionHistoryRepository,
)
from uow import BaseUnitOfWork


class DocumentUnitOfWork(BaseUnitOfWork):

    async def __aenter__(self):
        await super().__aenter__()
        self.repository = DocumentRepository(self.session)
        self.version_history_repository = VersionHistoryRepository(self.session)
        self.document_history_repository = DocumentHistoryRepository(self.session)
        return self

    async def flush(self):
        await self.session.flush()
