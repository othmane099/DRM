from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)


class User(BaseEntity):
    __tablename__ = "users"

    username = Column(String(255), nullable=True)
    documents = relationship("Document", back_populates="user")


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
