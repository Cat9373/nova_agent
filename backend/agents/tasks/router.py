from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.schemas.tasks import TaskCreate, TaskUpdate, TaskResponse
from backend.services.auth import get_current_user
from backend.database.models import User
from backend.services.task import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks Agent"])

@router.get("", response_model=List[TaskResponse])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return task_service.get_user_tasks(db, user_id=current_user.id, skip=skip, limit=limit)

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    payload: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return task_service.create_task(db, task_in=payload, user_id=current_user.id)

@router.patch("/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: str,
    payload: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = task_service.update_task(db, task_id=task_id, task_in=payload, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = task_service.delete_task(db, task_id=task_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
