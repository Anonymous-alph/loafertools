from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID

from .base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_model import User

class FeedbackBase(SQLModel):
    feedback_type: str  # "bug" | "feature" | "general"
    subject: str = Field(max_length=255)
    message: str
    rating: int | None = Field(default=None, ge=1, le=5)

class Feedback(BaseUUIDModel, FeedbackBase, table=True):
    __tablename__ = "feedbacks"

    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    user: "User" = Relationship(back_populates="feedbacks")