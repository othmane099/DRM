from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import settings
from auth.services import AuthService
from categories.services import CategoryService, SubCategoryService
from categories.uow import CategoryUnitOfWork, SubCategoryUnitOfWork
from documents.services import DocumentService
from documents.uow import DocumentUnitOfWork
from tags.services import TagService
from tags.uow import TagUnitOfWork
from users.services import PermissionService, RoleService, UserService
from users.uow import PermissionUnitOfWork, RoleUnitOfWork, UserUnitOfWork

engine = create_async_engine(settings.DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)


def default_session_factory():
    return async_session(bind=engine, autocommit=False, expire_on_commit=False)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["auth", "users", "categories", "tags", "documents"]
    )

    DEFAULT_SESSION_FACTORY = default_session_factory

    user_uow = providers.Factory(
        UserUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    user_service = providers.Factory(
        UserService,
        uow=user_uow,
    )

    permission_uow = providers.Factory(
        PermissionUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    permission_service = providers.Factory(
        PermissionService,
        uow=permission_uow,
    )

    role_uow = providers.Factory(
        RoleUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    role_service = providers.Factory(
        RoleService, uow=role_uow, permission_service=permission_service
    )

    auth_service = providers.Factory(AuthService, user_service=user_service)

    document_uow = providers.Factory(
        DocumentUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    document_service = providers.Factory(DocumentService, uow=document_uow)

    category_uow = providers.Factory(
        CategoryUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    category_service = providers.Factory(CategoryService, uow=category_uow)

    sub_category_uow = providers.Factory(
        SubCategoryUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    sub_category_service = providers.Factory(
        SubCategoryService, uow=sub_category_uow, document_service=document_service
    )

    tag_uow = providers.Factory(TagUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY)
    tag_service = providers.Factory(TagService, uow=tag_uow)
