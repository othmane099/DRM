from typing import Optional

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Document


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_document(self, data: dict) -> Optional[Document]:
        stmt = insert(Document).values(**data).returning(Document)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
