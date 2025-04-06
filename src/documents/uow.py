from documents.repositories import (
    DocumentCommentRepository,
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
        self.document_comment_repository = DocumentCommentRepository(self.session)
        return self

    async def flush(self):
        await self.session.flush()
