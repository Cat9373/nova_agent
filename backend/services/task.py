from typing import List, Optional
from sqlalchemy.orm import Session
from backend.database.models import Task
from backend.repositories.task import task_repository
from backend.schemas.tasks import TaskCreate, TaskUpdate
from backend.services.memory import memory_service

class TaskService:
    def get_task(self, db: Session, *, task_id: str, user_id: str) -> Optional[Task]:
        task = task_repository.get(db, id=task_id)
        if task and task.user_id == user_id:
            return task
        return None

    def get_user_tasks(self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
        return task_repository.get_by_user(db, user_id=user_id, skip=skip, limit=limit)

    def create_task(self, db: Session, *, task_in: TaskCreate, user_id: str) -> Task:
        # Create task db object
        db_obj = Task(
            user_id=user_id,
            title=task_in.title,
            description=task_in.description,
            due_date=task_in.due_date,
            status=task_in.status,
            priority=task_in.priority
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Index high priority or deadline tasks in Long Term Memory
        if db_obj.priority == "high" or db_obj.due_date is not None:
            memory_content = f"Task Deadline alert: '{db_obj.title}' due on {db_obj.due_date}. Details: {db_obj.description or ''}"
            memory_service.add_memory(
                db, 
                user_id=user_id, 
                category="task", 
                source_id=db_obj.id, 
                content=memory_content
            )
            
        return db_obj

    def update_task(self, db: Session, *, task_id: str, task_in: TaskUpdate, user_id: str) -> Optional[Task]:
        task = self.get_task(db, task_id=task_id, user_id=user_id)
        if not task:
            return None
        updated_task = task_repository.update(db, db_obj=task, obj_in=task_in)
        
        # Update or sync long term memory index
        if updated_task.priority == "high" or updated_task.due_date is not None:
            memory_content = f"Updated Task: '{updated_task.title}' status is '{updated_task.status}' due on {updated_task.due_date}. Priority: {updated_task.priority}."
            memory_service.add_memory(
                db, 
                user_id=user_id, 
                category="task", 
                source_id=updated_task.id, 
                content=memory_content
            )
        else:
            # Delete from memory if it is no longer high priority or having deadline
            memory_service.delete_memory_by_source(db, user_id=user_id, source_id=task_id, category="task")
            
        return updated_task

    def delete_task(self, db: Session, *, task_id: str, user_id: str) -> bool:
        task = self.get_task(db, task_id=task_id, user_id=user_id)
        if not task:
            return False
        task_repository.remove(db, id=task_id)
        # Clear long term memory trigger for this task
        memory_service.delete_memory_by_source(db, user_id=user_id, source_id=task_id, category="task")
        return True

task_service = TaskService()
