from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class MemoryBase(BaseModel):
    category: str  # meeting, calendar, note, task, preference, document
    source_id: str
    content: str

class MemoryCreate(MemoryBase):
    embedding: Optional[List[float]] = None

class MemoryResponse(MemoryBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MemorySearchQuery(BaseModel):
    query: str
    limit: int = 5
    category: Optional[str] = None
