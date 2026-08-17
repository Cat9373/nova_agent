from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from backend.database.models import CalendarEvent
from backend.repositories.base import BaseRepository

class CalendarEventRepository(BaseRepository[CalendarEvent]):
    def get_by_user(self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100) -> List[CalendarEvent]:
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()

    def get_upcoming_events(self, db: Session, *, user_id: str, start_after: datetime) -> List[CalendarEvent]:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.start_time >= start_after
        ).order_by(self.model.start_time.asc()).all()

calendar_event_repository = CalendarEventRepository(CalendarEvent)
