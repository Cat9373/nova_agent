from sqlalchemy.orm import Session
from backend.database.models import User, Profile
from backend.repositories.user import user_repository
from backend.repositories.profile import profile_repository
from backend.schemas.user import UserCreate

class UserService:
    def create_user(self, db: Session, *, user_in: UserCreate) -> User:
        user = user_repository.create_local(db, email=user_in.email, password=user_in.password)
        # Auto-create empty profile
        profile = Profile(user_id=user.id, first_name="", last_name="")
        db.add(profile)
        db.commit()
        db.refresh(user)
        return user

    def get_user_by_email(self, db: Session, *, email: str) -> User:
        return user_repository.get_by_email(db, email=email)

user_service = UserService()
