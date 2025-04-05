from dependency_injector.wiring import Provide

from auth.schemas import TokenUserPayload
from models import Tag
from tags.schemas import TagCreate, TagUpdate
from tags.uow import TagUnitOfWork


class TagService:

    def __init__(self, uow: TagUnitOfWork = Provide["tag_uow"]):
        self.uow = uow

    async def count_tags(self) -> int:
        async with self.uow:
            return await self.uow.repository.count_tags()

    async def get_tags(self, page: int, size: int) -> list[Tag]:
        async with self.uow:
            return await self.uow.repository.get_tags(page, size)

    async def create_tag(
        self, current_user: TokenUserPayload, tag_create: TagCreate
    ) -> Tag:
        data = tag_create.model_dump()
        data["parent_id"] = current_user.id
        async with self.uow:
            tag = await self.uow.repository.create_tag(data)
            await self.uow.commit()
            return tag

    async def update_tag(self, tag_id: int, tag_update: TagUpdate) -> Tag:
        async with self.uow:
            data = {k: v for k, v in tag_update.model_dump().items() if v is not None}
            tag = await self.uow.repository.update_tag(tag_id, data)
            await self.uow.commit()
            return tag

    async def delete_tag(self, tag_id: int):
        async with self.uow:
            await self.uow.repository.delete_tag(tag_id)
            await self.uow.commit()
