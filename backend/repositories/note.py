from typing import List
from sqlalchemy.orm import Session
from backend.database.models import Note
from backend.repositories.base import BaseRepository

class NoteRepository(BaseRepository[Note]):
    def get_by_user(self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100) -> List[Note]:
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()

    def get_important(self, db: Session, *, user_id: str) -> List[Note]:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.is_important == True
        ).all()

note_repository = NoteRepository(Note)
