from typing import Optional
from sqlalchemy.orm import Session
from backend.database.models import User
from backend.repositories.base import BaseRepository
from backend.core.security import get_password_hash

class UserRepository(BaseRepository[User]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def create_local(self, db: Session, *, email: str, password: str) -> User:
        hashed_password = get_password_hash(password)
        db_obj = User(email=email, hashed_password=hashed_password)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user_repository = UserRepository(User)
