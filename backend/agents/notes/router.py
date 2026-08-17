from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.schemas.notes import NoteCreate, NoteUpdate, NoteResponse
from backend.services.auth import get_current_user
from backend.database.models import User
from backend.services.note import note_service

router = APIRouter(prefix="/notes", tags=["Notes Agent"])

@router.get("", response_model=List[NoteResponse])
def read_notes(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return note_service.get_user_notes(db, user_id=current_user.id, skip=skip, limit=limit)

@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_new_note(
    payload: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return note_service.create_note(db, note_in=payload, user_id=current_user.id)

@router.patch("/{note_id}", response_model=NoteResponse)
def update_existing_note(
    note_id: str,
    payload: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = note_service.update_note(db, note_id=note_id, note_in=payload, user_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = note_service.delete_note(db, note_id=note_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return None
