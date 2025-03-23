from dependency_injector.wiring import Provide

from auth.schemas import TokenUserPayload
from models import Tag
from tags.schemas import TagCreate
from tags.uow import TagUnitOfWork


class TagService:

    def __init__(self, uow: TagUnitOfWork = Provide["tag_uow"]):
        self.uow = uow

    async def create_tag(
        self, current_user: TokenUserPayload, tag_create: TagCreate
    ) -> Tag:
        data = tag_create.model_dump()
        data["parent_id"] = current_user.id
        async with self.uow:
            tag = await self.uow.repository.create_tag(data)
            await self.uow.commit()
            return tag
