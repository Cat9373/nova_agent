from typing import List, Optional
from sqlalchemy.orm import Session
from backend.database.models import Meeting
from backend.repositories.base import BaseRepository

class MeetingRepository(BaseRepository[Meeting]):
    def get_by_user(self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100) -> List[Meeting]:
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()

meeting_repository = MeetingRepository(Meeting)
