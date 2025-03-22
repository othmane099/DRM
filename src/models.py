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
    parent_id = Column(Integer, default=0)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_owner = Column(Boolean, default=False, nullable=False)
    avatar = Column(String, nullable=True)

    role = relationship("Role", back_populates="users")
    documents = relationship("Document", back_populates="user")


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

    title = Column(String(255), nullable=True)
    parent_id = Column(Integer, default=0)
    sub_categories = relationship("SubCategory", back_populates="category")
    documents = relationship("Document", back_populates="category")


class SubCategory(BaseEntity):
    __tablename__ = "sub_categories"

    title = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    parent_id = Column(Integer, default=0)
    category = relationship("Category", back_populates="sub_categories")
    documents = relationship("Document", back_populates="sub_category")


class Tag(BaseEntity):
    __tablename__ = "tags"

    title = Column(String(255), nullable=True)
    parent_id = Column(Integer, default=0)


class Document(BaseEntity):
    __tablename__ = "documents"

    name = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    sub_category_id = Column(Integer, ForeignKey("sub_categories.id"), nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(String(255), nullable=True)
    parent_id = Column(Integer, default=0)

    category = relationship("Category", back_populates="documents")
    sub_category = relationship("SubCategory", back_populates="documents")
    user = relationship("User", back_populates="documents")
