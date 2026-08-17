from sqlalchemy.orm import Session
from backend.database.session import SessionLocal
from backend.services.note import note_service
from backend.schemas.notes import NoteCreate
from backend.utils.logging import logger

class NotesAgentService:
    def process_note_intent(self, prompt: str, user_id: str) -> str:
        """
        Parses prompts related to notes and coordinates actions.
        For a production-grade agent, this parses structured parameters from prompts
        and invokes NoteService database methods.
        """
        logger.info(f"NotesAgent processing: '{prompt}'")
        db: Session = SessionLocal()
        try:
            # Basic parsing heuristic (in future steps, this utilizes LangChain function calling)
            if "create" in prompt.lower() or "write" in prompt.lower() or "save" in prompt.lower():
                # Extract simple title and content mocks
                content = prompt.replace("create note", "").replace("save note", "").strip()
                title = "AI Note"
                if ":" in content:
                    parts = content.split(":", 1)
                    title = parts[0].strip()
                    content = parts[1].strip()
                
                note_in = NoteCreate(title=title, content=content or prompt, is_important=True)
                note = note_service.create_note(db, note_in=note_in, user_id=user_id)
                return f"I have successfully created an important note titled '{note.title}' and indexed it in your long term memory."
                
            elif "list" in prompt.lower() or "get" in prompt.lower() or "show" in prompt.lower():
                notes = note_service.get_user_notes(db, user_id=user_id)
                if not notes:
                    return "You do not have any notes recorded yet."
                summary = "Here are your notes:\n"
                for idx, note in enumerate(notes, 1):
                    summary += f"{idx}. [{note.title}]: {note.content[:60]} (Important: {note.is_important})\n"
                return summary
            else:
                return "I detected a Notes query. Try typing 'create note: [title]: [content]' or 'list notes'."
        finally:
            db.close()

notes_agent_service = NotesAgentService()
