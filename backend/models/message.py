"""
Message model for the Todo application
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid


class MessageBase(SQLModel):
    role: str = Field(max_length=20)  # 'user', 'assistant', 'system'
    content: str = Field(max_length=5000)


class Message(MessageBase, table=True):
    __tablename__ = "messages"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    pass


class MessageUpdate(SQLModel):
    content: Optional[str] = Field(default=None, max_length=5000)


class MessagePublic(MessageBase):
    id: uuid.UUID
    conversation_id: uuid.UUID
    created_at: datetime