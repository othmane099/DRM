from typing import Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Document, VersionHistory


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_document(self, data: dict) -> Optional[Document]:
        stmt = insert(Document).values(**data).returning(Document)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class VersionHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_version_history(self, data: dict) -> Optional[VersionHistory]:
        stmt = insert(VersionHistory).values(**data).returning(VersionHistory)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_versions_by_document(self, document_id: int) -> list[VersionHistory]:
        result = await self.session.scalars(
            select(VersionHistory).where(VersionHistory.document_id == document_id)
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
