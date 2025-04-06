from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)


class User(BaseEntity):
    __tablename__ = "users"
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    avatar = Column(String, nullable=True)

    role = relationship("Role", back_populates="users")
    documents = relationship("Document", back_populates="user")
    version_histories = relationship("VersionHistory", back_populates="user")
    document_histories = relationship("DocumentHistory", back_populates="user")


role_permission = Table(
    "roles_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id")),
)


class Role(BaseEntity):
    __tablename__ = "roles"

    name = Column(String, unique=True, nullable=False)
    users = relationship("User", back_populates="role")
    permissions = relationship(
        "Permission", secondary=role_permission, back_populates="roles"
    )


class Permission(BaseEntity):
    __tablename__ = "permissions"

    name = Column(String, unique=True, nullable=False)
    label = Column(String, unique=True, nullable=False)
    roles = relationship(
        "Role", secondary=role_permission, back_populates="permissions"
    )


class Category(BaseEntity):
    __tablename__ = "categories"

    title = Column(String(255), nullable=True, unique=True)
    sub_categories = relationship("SubCategory", back_populates="category")
    documents = relationship("Document", back_populates="category")


class SubCategory(BaseEntity):
    __tablename__ = "sub_categories"

    title = Column(String(255), nullable=True, unique=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="sub_categories")
    documents = relationship("Document", back_populates="sub_category")


class Tag(BaseEntity):
    __tablename__ = "tags"

    title = Column(String(255), nullable=True)


class Document(BaseEntity):
    __tablename__ = "documents"

    name = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    sub_category_id = Column(Integer, ForeignKey("sub_categories.id"), nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(String(255), nullable=True)

    category = relationship("Category", back_populates="documents")
    sub_category = relationship("SubCategory", back_populates="documents")
    user = relationship("User", back_populates="documents")
    version_histories = relationship("VersionHistory", back_populates="document")
    document_histories = relationship("DocumentHistory", back_populates="document")


class VersionHistory(BaseEntity):
    __tablename__ = "version_histories"

    document_id = Column(
        Integer, ForeignKey("documents.id", ondelete="SET NULL"), nullable=True
    )
    document_name = Column(String, nullable=True)
    current_version = Column(Boolean, default=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="version_histories")
    document = relationship("Document", back_populates="version_histories")


class DocumentHistory(BaseEntity):
    __tablename__ = "document_histories"

    document_id = Column(
        Integer, ForeignKey("documents.id", ondelete="SET NULL"), nullable=True
    )
    action = Column(String, nullable=True)
    action_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=True)

    user = relationship("User", back_populates="document_histories")
    document = relationship("Document", back_populates="document_histories")
