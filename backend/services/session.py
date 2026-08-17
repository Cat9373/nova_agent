from typing import List, Optional
from sqlalchemy.orm import Session
from backend.database.models import ConversationSession
from backend.repositories.session import session_repository
from backend.schemas.chat import ChatSessionCreate

class SessionService:
    def get_session(self, db: Session, *, session_id: str, user_id: str) -> Optional[ConversationSession]:
        return session_repository.get_by_user_and_id(db, user_id=user_id, session_id=session_id)

    def get_user_sessions(self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100) -> List[ConversationSession]:
        return session_repository.get_by_user(db, user_id=user_id, skip=skip, limit=limit)

    def create_session(self, db: Session, *, session_in: ChatSessionCreate, user_id: str) -> ConversationSession:
        db_obj = ConversationSession(
            user_id=user_id,
            title=session_in.title or "New Conversation"
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_session(self, db: Session, *, session_id: str, user_id: str) -> bool:
        session = self.get_session(db, session_id=session_id, user_id=user_id)
        if not session:
            return False
        session_repository.remove(db, id=session_id)
        return True

session_service = SessionService()
