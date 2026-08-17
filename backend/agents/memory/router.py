from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.schemas.memory import MemoryResponse, MemorySearchQuery
from backend.services.auth import get_current_user
from backend.database.models import User
from backend.services.memory import memory_service

router = APIRouter(prefix="/memory", tags=["Memory Agent"])

@router.post("/search", response_model=List[MemoryResponse])
def search_user_memories(
    payload: MemorySearchQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search over user's long-term memory (important tasks, notes, documents, events).
    """
    try:
        return memory_service.search_memories(
            db, 
            user_id=current_user.id, 
            query=payload.query, 
            category=payload.category, 
            limit=payload.limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
