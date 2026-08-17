from typing import List, Optional
from sqlalchemy.orm import Session
from backend.database.models import Note
from backend.repositories.note import note_repository
from backend.schemas.notes import NoteCreate, NoteUpdate
from backend.services.memory import memory_service

class NoteService:
    def get_note(self, db: Session, *, note_id: str, user_id: str) -> Optional[Note]:
        note = note_repository.get(db, id=note_id)
        if note and note.user_id == user_id:
            return note
        return None

    def get_user_notes(self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100) -> List[Note]:
        return note_repository.get_by_user(db, user_id=user_id, skip=skip, limit=limit)

    def create_note(self, db: Session, *, note_in: NoteCreate, user_id: str) -> Note:
        db_obj = Note(
            user_id=user_id,
            title=note_in.title,
            content=note_in.content,
            is_important=note_in.is_important
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Index important notes in memory
        if db_obj.is_important:
            memory_content = f"Important Note: '{db_obj.title}' - Content: {db_obj.content}"
            memory_service.add_memory(
                db, 
                user_id=user_id, 
                category="note", 
                source_id=db_obj.id, 
                content=memory_content
            )
            
        return db_obj

    def update_note(self, db: Session, *, note_id: str, note_in: NoteUpdate, user_id: str) -> Optional[Note]:
        note = self.get_note(db, note_id=note_id, user_id=user_id)
        if not note:
            return None
        updated_note = note_repository.update(db, db_obj=note, obj_in=note_in)
        
        # Sync with Long-term memory
        if updated_note.is_important:
            memory_content = f"Important Note: '{updated_note.title}' - Content: {updated_note.content}"
            memory_service.add_memory(
                db, 
                user_id=user_id, 
                category="note", 
                source_id=updated_note.id, 
                content=memory_content
            )
        else:
            # Delete if no longer important
            memory_service.delete_memory_by_source(db, user_id=user_id, source_id=note_id, category="note")
            
        return updated_note

    def delete_note(self, db: Session, *, note_id: str, user_id: str) -> bool:
        note = self.get_note(db, note_id=note_id, user_id=user_id)
        if not note:
            return False
        note_repository.remove(db, id=note_id)
        memory_service.delete_memory_by_source(db, user_id=user_id, source_id=note_id, category="note")
        return True

note_service = NoteService()
