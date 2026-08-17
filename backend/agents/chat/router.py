from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.schemas.chat import ChatMessageRequest, ChatMessageResponse
from backend.services.auth import get_current_user
from backend.database.models import User
from backend.agents.orchestrator.graph import master_orchestrator

router = APIRouter(prefix="/chat", tags=["AI Chat"])

@router.post("/message", response_model=ChatMessageResponse)
def post_chat_message(
    payload: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submits user query to the Master AI Orchestrator to decide routing
    and execute LLM actions.
    """
    try:
        response_text = master_orchestrator.execute(
            user_id=current_user.id,
            session_id=payload.session_id,
            prompt=payload.content
        )
        return ChatMessageResponse(
            response=response_text,
            session_id=payload.session_id,
            suggestions=["Remind me tomorrow at 9 AM", "Create a new task", "Search my uploaded PDFs"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
