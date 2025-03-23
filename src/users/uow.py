from uow import BaseUnitOfWork
from users.repositories import PermissionRepository, RoleRepository, UserRepository


class UserUnitOfWork(BaseUnitOfWork):

    async def __aenter__(self):
        await super().__aenter__()
        self.repository = UserRepository(self.session)
        return self


class RoleUnitOfWork(BaseUnitOfWork):

    async def __aenter__(self):
        await super().__aenter__()
        self.repository = RoleRepository(self.session)
        return self


class PermissionUnitOfWork(BaseUnitOfWork):

    async def __aenter__(self):
        await super().__aenter__()
        self.repository = PermissionRepository(self.session)
        return self
