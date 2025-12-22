from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from datetime import datetime

from .base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_model import User

class ChatMessageBase(SQLModel):
    role: str  # "user" | "assistant"
    content: str
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    session_id: UUID | None = None  # Group messages by conversation session

class ChatMessage(BaseUUIDModel, ChatMessageBase, table=True):
    __tablename__ = "chat_messages"

    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    user: "User" = Relationship(back_populates="chat_messages")