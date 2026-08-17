from typing import List, Optional
from sqlalchemy.orm import Session
from backend.database.models import ConversationSession
from backend.repositories.base import BaseRepository

class SessionRepository(BaseRepository[ConversationSession]):
    def get_by_user(self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100) -> List[ConversationSession]:
        return db.query(self.model).filter(self.model.user_id == user_id).order_by(self.model.updated_at.desc()).offset(skip).limit(limit).all()

    def get_by_user_and_id(self, db: Session, *, user_id: str, session_id: str) -> Optional[ConversationSession]:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.id == session_id
        ).first()

session_repository = SessionRepository(ConversationSession)
