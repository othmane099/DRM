import os
import pathlib
import time
from typing import Optional

from dependency_injector.wiring import Provide
from fastapi import UploadFile

from auth.schemas import TokenUserPayload
from documents.schemas import (
    DocumentCreate,
    DocumentHistoryCreate,
    DocumentUpdate,
    VersionHistoryCreate,
)
from documents.uow import DocumentUnitOfWork
from models import Document


class DocumentService:

    def __init__(self, uow: DocumentUnitOfWork = Provide["document_uow"]):
        self.uow = uow

    async def create_document(
        self,
        current_user: TokenUserPayload,
        document_create: DocumentCreate,
        file: UploadFile,
    ):
        data = document_create.model_dump()
        data["tags"] = ",".join(data["tags"]) if data["tags"] else ""
        async with self.uow:
            created_document = await self.uow.repository.create_document(data)
            await self.uow.flush()
            if file:
                filename = file.filename
                file_extension = pathlib.Path(filename).suffix
                document_file_name = f"{int(time.time())}{file_extension}"

                upload_dir = os.path.join("upload", "documents")
                os.makedirs(upload_dir, exist_ok=True)

                file_path = os.path.join(upload_dir, document_file_name)

                with open(file_path, "wb") as f:
                    content = await file.read()
                    f.write(content)

                version_create = VersionHistoryCreate(
                    document_id=created_document.id,
                    document_name=created_document.name,
                    current_version=True,
                    created_by=current_user.id,
                )
                await self.uow.version_history_repository.create_version_history(
                    version_create.model_dump()
                )
            document_history_create = DocumentHistoryCreate(
                document_id=created_document.id,
                action="Document Create",
                description=f"New document {created_document.name} created by {current_user.email}",
                action_by=current_user.id,
            )
            await self.uow.document_history_repository.create_document_history(
                document_history_create.model_dump()
            )
            await self.uow.commit()
            return created_document

    async def update_document(
        self,
        current_user: TokenUserPayload,
        document_id: int,
        document_update: DocumentUpdate,
    ):
        async with self.uow:
            data = {
                k: v for k, v in document_update.model_dump().items() if v is not None
            }
            if data.get("tags", None):
                data["tags"] = ",".join(data["tags"])

            document_name = await self.uow.repository.get_document_name(document_id)
            updated_document = await self.uow.repository.update_document(
                document_id, data
            )
            document_history_create = DocumentHistoryCreate(
                document_id=document_id,
                action="Document Update",
                description=f"Document {document_name} updated by {current_user.email}",
                action_by=current_user.id,
            )
            await self.uow.document_history_repository.create_document_history(
                document_history_create.model_dump()
            )
            await self.uow.commit()
            return updated_document

    async def get_document_versions(self, document_id):
        async with self.uow:
            return await self.uow.version_history_repository.get_versions_by_document(
                document_id
            )

    async def create_document_version(
        self, version_create: VersionHistoryCreate, file: UploadFile
    ):
        async with self.uow:
            last_version = await self.uow.version_history_repository.get_current_version_by_document(
                version_create.document_id
            )
            if last_version:
                last_version.current_version = False

            filename = file.filename
            file_extension = pathlib.Path(filename).suffix
            document_file_name = f"{int(time.time())}{file_extension}"

            upload_dir = os.path.join("upload", "documents")
            os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(upload_dir, document_file_name)

            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            document_name = await self.uow.repository.get_document_name(
                version_create.document_id
            )
            data = version_create.model_dump()
            data["document_name"] = document_name
            version = await self.uow.version_history_repository.create_version_history(
                data
            )
            await self.uow.commit()
            return version

    async def get_document_history_by_user(self, user_id: int):
        async with self.uow:
            return (
                await self.uow.document_history_repository.get_document_history_by_user(
                    user_id
                )
            )

    async def delete_document(self, current_user: TokenUserPayload, document_id: int):
        async with self.uow:
            document_name = await self.uow.repository.get_document_name(document_id)
            document_history_create = DocumentHistoryCreate(
                document_id=document_id,
                action="Document Delete",
                description=f"Document {document_name} deleted by {current_user.email}",
                action_by=current_user.id,
            )
            await self.uow.document_history_repository.create_document_history(
                document_history_create.model_dump()
            )
            await self.uow.repository.delete_document(document_id)
            await self.uow.commit()

    async def get_documents_by_user(self, user_id: int):
        async with self.uow:
            return await self.uow.repository.get_documents_by_user(user_id)

    async def get_first_document_by_subcategory(self, sc_id: int) -> Optional[Document]:
        async with self.uow:
            return await self.uow.repository.get_first_document_by_subcategory(sc_id)
