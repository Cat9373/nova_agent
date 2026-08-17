from typing import List
from sqlalchemy.orm import Session
from backend.database.models import Task
from backend.repositories.base import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def get_by_user(self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()

    def get_by_status(self, db: Session, *, user_id: str, status: str) -> List[Task]:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.status == status
        ).all()

task_repository = TaskRepository(Task)
