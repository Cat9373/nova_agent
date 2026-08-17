from typing import List, Optional
from sqlalchemy.orm import Session
from backend.database.models import Memory
from backend.repositories.memory import memory_repository
from backend.rag.embeddings.service import embedding_service
from backend.schemas.memory import MemoryCreate
from backend.utils.logging import logger

class MemoryService:
    def add_memory(
        self, 
        db: Session, 
        *, 
        user_id: str, 
        category: str, 
        source_id: str, 
        content: str
    ) -> Memory:
        """
        Extracts semantic text, generates embeddings, and saves it in long term memory.
        """
        logger.info(f"Adding long-term memory for user {user_id} in category {category}")
        vector = embedding_service.get_embedding(content)
        
        # Check if memory for this source_id already exists to prevent duplicate indexes
        existing_memories = db.query(Memory).filter(
            Memory.user_id == user_id,
            Memory.source_id == source_id,
            Memory.category == category
        ).all()
        
        for m in existing_memories:
            db.delete(m)
        db.commit()
            
        memory_in = MemoryCreate(
            category=category,
            source_id=source_id,
            content=content,
            embedding=vector
        )
        
        # Manually convert schema + inject user_id
        db_obj = Memory(
            user_id=user_id,
            category=memory_in.category,
            source_id=memory_in.source_id,
            content=memory_in.content,
            embedding=memory_in.embedding
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def search_memories(
        self, 
        db: Session, 
        *, 
        user_id: str, 
        query: str, 
        category: Optional[str] = None, 
        limit: int = 5
    ) -> List[Memory]:
        """
        Executes semantic search over memories.
        """
        query_vector = embedding_service.get_embedding(query)
        return memory_repository.search_semantic(
            db, 
            user_id=user_id, 
            query_embedding=query_vector, 
            category=category, 
            limit=limit
        )

    def delete_memory_by_source(self, db: Session, *, user_id: str, source_id: str, category: str) -> None:
        memories = db.query(Memory).filter(
            Memory.user_id == user_id,
            Memory.source_id == source_id,
            Memory.category == category
        ).all()
        for m in memories:
            db.delete(m)
        db.commit()

memory_service = MemoryService()
