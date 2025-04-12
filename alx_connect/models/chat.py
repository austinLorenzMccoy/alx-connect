from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_validator('content')
    def clean_content(cls, v):
        if not v or not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()

class ConversationState(BaseModel):
    messages: list[Message] = Field(default_factory=list)
    last_activity: datetime = Field(default_factory=datetime.now)
    active: bool = True

    class Config:
        arbitrary_types_allowed = True

class QuestionInput(BaseModel):
    question: str
    conversation_id: str | None = None

    @field_validator('question')
    def validate_question(cls, v):
        if not v or not v.strip():
            raise ValueError("Question cannot be empty")
        return v.strip() 