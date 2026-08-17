from fastapi import APIRouter, Depends, status
from backend.services.auth import get_current_user
from backend.database.models import User

router = APIRouter(tags=["Phase 2 Placeholder Endpoints"])

@router.get("/meetings", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_meetings_placeholder(current_user: User = Depends(get_current_user)):
    """
    [Phase 2 Feature Blueprint] Meeting transcription, summaries, and action item extractor.
    """
    return {
        "status": "planned",
        "phase": 2,
        "detail": "Meeting agent & transcription engine API contracts are planned for Phase 2."
    }

@router.get("/calendar", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_calendar_placeholder(current_user: User = Depends(get_current_user)):
    """
    [Phase 2 Feature Blueprint] Google Calendar & Microsoft Outlook schedule planner integration.
    """
    return {
        "status": "planned",
        "phase": 2,
        "detail": "Calendar schedules and integrations are planned for Phase 2."
    }

@router.get("/email", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_email_placeholder(current_user: User = Depends(get_current_user)):
    """
    [Phase 2 Feature Blueprint] Gmail & Outlook auto response assistant agents.
    """
    return {
        "status": "planned",
        "phase": 2,
        "detail": "Email assistant and workflow engines are planned for Phase 2."
    }
