from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatSessionCreate(BaseModel):
    title: Optional[str] = None

class ChatSessionResponse(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatMessageRequest(BaseModel):
    content: str
    session_id: str

class ChatMessageResponse(BaseModel):
    response: str
    session_id: str
    suggestions: Optional[List[str]] = None
