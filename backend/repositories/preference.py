from typing import List, Optional
from sqlalchemy.orm import Session
from backend.database.models import Preference
from backend.repositories.base import BaseRepository

class PreferenceRepository(BaseRepository[Preference]):
    def get_by_user(self, db: Session, *, user_id: str) -> List[Preference]:
        return db.query(self.model).filter(self.model.user_id == user_id).all()

    def get_by_key(self, db: Session, *, user_id: str, key: str) -> Optional[Preference]:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.key == key
        ).first()

    def set_preference(self, db: Session, *, user_id: str, key: str, value: str) -> Preference:
        pref = self.get_by_key(db, user_id=user_id, key=key)
        if pref:
            pref.value = value
            db.add(pref)
            db.commit()
            db.refresh(pref)
            return pref
        else:
            new_pref = Preference(user_id=user_id, key=key, value=value)
            db.add(new_pref)
            db.commit()
            db.refresh(new_pref)
            return new_pref

preference_repository = PreferenceRepository(Preference)
