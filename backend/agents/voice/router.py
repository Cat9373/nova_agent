from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from backend.schemas.voice import VoiceTranscriptResponse
from backend.services.auth import get_current_user
from backend.database.models import User
from backend.agents.voice.services import voice_agent_service
from backend.agents.orchestrator.graph import master_orchestrator

router = APIRouter(prefix="/voice", tags=["Voice Agent"])

@router.post("/transcribe", response_model=VoiceTranscriptResponse)
def transcribe_voice_input(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Accepts voice audio files and returns raw transcriptions.
    """
    try:
        content = file.file.read()
        transcript = voice_agent_service.transcribe_audio(content, file.filename)
        return VoiceTranscriptResponse(
            transcript=transcript,
            confidence=0.95,
            duration_seconds=3.5
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/command")
def process_voice_command(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Transcribes audio file and directly pipes transcript to the Master AI Orchestrator.
    """
    try:
        content = file.file.read()
        transcript = voice_agent_service.transcribe_audio(content, file.filename)
        # Process via LangGraph Orchestrator
        ai_response = master_orchestrator.execute(
            user_id=current_user.id,
            session_id="voice-session",
            prompt=transcript
        )
        return {
            "transcript": transcript,
            "ai_response": ai_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
