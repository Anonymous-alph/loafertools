from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID

from .base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_model import User

class ResourceBase(SQLModel):
    title: str = Field(max_length=255)
    url: str | None = None
    resource_type: str  
    notes: str | None = None
    is_favorite: bool = Field(default=False)

class Resource(BaseUUIDModel, ResourceBase, table=True):
    __tablename__ = "resources"

    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    user: "User" = Relationship(back_populates="resources")