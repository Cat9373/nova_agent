from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentBase(BaseModel):
    file_name: str
    mime_type: str
    file_size: int

class DocumentCreate(DocumentBase):
    file_path: str
    storage_provider: str = "local"

class DocumentResponse(DocumentBase):
    id: str
    user_id: str
    file_path: str
    storage_provider: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DocumentEmbeddingCreate(BaseModel):
    chunk_index: int
    text_content: str
    embedding: List[float]

class DocumentChatQuery(BaseModel):
    query: str
    document_ids: Optional[List[str]] = None
    limit: int = 4
