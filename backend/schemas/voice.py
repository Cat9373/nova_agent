from pydantic import BaseModel
from typing import Optional

class VoiceTranscriptResponse(BaseModel):
    transcript: str
    confidence: float
    duration_seconds: float

class VoiceProcessRequest(BaseModel):
    session_id: Optional[str] = None
    execute_intently: bool = True
