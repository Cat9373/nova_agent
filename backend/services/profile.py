from sqlalchemy.orm import Session
from backend.database.models import Profile
from backend.repositories.profile import profile_repository
from backend.schemas.profile import ProfileUpdate

class ProfileService:
    def get_profile(self, db: Session, *, user_id: str) -> Profile:
        profile = profile_repository.get_by_user_id(db, user_id=user_id)
        if not profile:
            # Create if not exists
            profile = Profile(user_id=user_id, first_name="", last_name="")
            db.add(profile)
            db.commit()
            db.refresh(profile)
        return profile

    def update_profile(self, db: Session, *, user_id: str, profile_in: ProfileUpdate) -> Profile:
        profile = self.get_profile(db, user_id=user_id)
        return profile_repository.update(db, db_obj=profile, obj_in=profile_in)

profile_service = ProfileService()
