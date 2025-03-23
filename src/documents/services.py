import os
import pathlib
import time

from dependency_injector.wiring import Provide
from fastapi import UploadFile

from auth.schemas import TokenUserPayload
from documents.schemas import DocumentCreate
from documents.uow import DocumentUnitOfWork


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
        # TODO replace 1 by parent_id
        data["parent_id"] = (
            current_user.id if current_user.is_superuser or current_user.is_admin else 1
        )
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
            await self.uow.commit()
            return created_document
