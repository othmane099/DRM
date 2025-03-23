import abc
from typing import Any, Callable

from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork(abc.ABC, metaclass=abc.ABCMeta):

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError  # pragma: no cover


class BaseUnitOfWork(UnitOfWork):

    @inject
    def __init__(
        self,
        session_factory: Callable[[], Any] = Provide["DEFAULT_SESSION_FACTORY"],
    ):
        self.session_factory = session_factory()

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.aclose()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
