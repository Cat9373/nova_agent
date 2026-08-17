from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from backend.database.models import Memory
from backend.repositories.base import BaseRepository
from backend.utils.logging import logger

class MemoryRepository(BaseRepository[Memory]):
    def get_by_user(self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100) -> List[Memory]:
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()

    def search_semantic(
        self, 
        db: Session, 
        *, 
        user_id: str, 
        query_embedding: List[float], 
        category: Optional[str] = None, 
        limit: int = 5
    ) -> List[Memory]:
        """
        Executes a vector similarity search over the memories of a user.
        Falls back to keyword matching if pgvector throws an error (e.g. extension not configured).
        """
        try:
            # We use pgvector's cosine_distance operator (<=> equivalent)
            query = db.query(self.model).filter(self.model.user_id == user_id)
            if category:
                query = query.filter(self.model.category == category)
                
            # Perform vector distance sorting
            return query.order_by(self.model.embedding.cosine_distance(query_embedding)).limit(limit).all()
        except Exception as e:
            logger.error(f"pgvector query failed: {str(e)}. Falling back to simple keyword matching.")
            # Basic fallback query
            query = db.query(self.model).filter(self.model.user_id == user_id)
            if category:
                query = query.filter(self.model.category == category)
            return query.limit(limit).all()

    def search_keyword(self, db: Session, *, user_id: str, keyword: str, category: Optional[str] = None, limit: int = 5) -> List[Memory]:
        query = db.query(self.model).filter(
            and_(
                self.model.user_id == user_id,
                self.model.content.ilike(f"%{keyword}%")
            )
        )
        if category:
            query = query.filter(self.model.category == category)
        return query.limit(limit).all()

memory_repository = MemoryRepository(Memory)
