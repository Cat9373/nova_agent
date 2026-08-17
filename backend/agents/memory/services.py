from sqlalchemy.orm import Session
from backend.database.session import SessionLocal
from backend.services.memory import memory_service
from backend.utils.logging import logger

class MemoryAgentService:
    def process_memory_query(self, prompt: str, user_id: str) -> str:
        """
        Interacts with the long term memory indexes.
        Queries memories semantically.
        """
        logger.info(f"MemoryAgent searching memories: '{prompt}'")
        db: Session = SessionLocal()
        try:
            memories = memory_service.search_memories(db, user_id=user_id, query=prompt, limit=4)
            if not memories:
                return "I couldn't recall any past meetings, tasks, notes, or preferences relating to that."
                
            summary = "Here is what I recall from your long-term memory:\n"
            for idx, mem in enumerate(memories, 1):
                summary += f"{idx}. [{mem.category.upper()}]: {mem.content}\n"
            return summary
        finally:
            db.close()

memory_agent_service = MemoryAgentService()
