from typing import Optional
from sqlalchemy.orm import Session
from backend.database.models import Profile
from backend.repositories.base import BaseRepository

class ProfileRepository(BaseRepository[Profile]):
    def get_by_user_id(self, db: Session, *, user_id: str) -> Optional[Profile]:
        return db.query(self.model).filter(self.model.user_id == user_id).first()

profile_repository = ProfileRepository(Profile)
