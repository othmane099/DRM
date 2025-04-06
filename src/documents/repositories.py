from typing import Optional

from sqlalchemy import delete, desc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Document, DocumentComment, DocumentHistory, VersionHistory


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_document_name(self, document_id: int) -> Optional[str]:
        result = await self.session.scalars(
            select(Document.name).where(Document.id == document_id)
        )
        return result.first()

    async def create_document(self, data: dict) -> Optional[Document]:
        stmt = insert(Document).values(**data).returning(Document)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_document(self, document_id: int):
        await self.session.execute(delete(Document).where(Document.id == document_id))

    async def get_documents_by_user(self, user_id: int) -> list[Document]:
        result = await self.session.scalars(
            select(Document)
            .where(Document.user_id == user_id)
            .order_by(desc(Document.created_at))
        )
        return list(result.all())

    async def update_document(self, document_id: int, data: dict) -> Optional[Document]:
        stmt = (
            update(Document)
            .where(Document.id == document_id)
            .values(**data)
            .returning(Document)
        )

        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one_or_none()

    async def get_first_document_by_subcategory(self, sc_id: int) -> Optional[Document]:
        result = await self.session.scalars(
            select(Document).where(Document.sub_category_id == sc_id)
        )
        return result.first()


class VersionHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_version_history(self, data: dict) -> Optional[VersionHistory]:
        stmt = insert(VersionHistory).values(**data).returning(VersionHistory)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_versions_by_document(self, document_id: int) -> list[VersionHistory]:
        result = await self.session.scalars(
            select(VersionHistory)
            .where(VersionHistory.document_id == document_id)
            .order_by(desc(VersionHistory.created_at))
        )
        return list(result.all())

    async def get_current_version_by_document(
        self, document_id: int
    ) -> Optional[VersionHistory]:
        result = await self.session.scalars(
            select(VersionHistory).where(
                VersionHistory.document_id == document_id,
                VersionHistory.current_version == True,
            )
        )
        return result.first()


class DocumentHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_document_history(self, data: dict) -> Optional[DocumentHistory]:
        stmt = insert(DocumentHistory).values(**data).returning(DocumentHistory)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_document_history_by_user(self, user_id: int) -> list[DocumentHistory]:
        result = await self.session.scalars(
            select(DocumentHistory)
            .where(
                DocumentHistory.action_by == user_id,
            )
            .order_by(desc(DocumentHistory.created_at))
        )
        return list(result.all())


class DocumentCommentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_document_comments(self, document_id: int) -> list[DocumentComment]:
        result = await self.session.scalars(
            select(DocumentComment)
            .where(DocumentComment.document_id == document_id)
            .order_by(DocumentComment.created_at)
        )
        return list(result.all())

    async def create_document_comment(self, data: dict) -> Optional[DocumentComment]:
        stmt = insert(DocumentComment).values(**data).returning(DocumentComment)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
