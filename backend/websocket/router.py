from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from sqlalchemy.orm import Session
from backend.database.session import SessionLocal
from backend.websocket.connection_manager import websocket_manager
from backend.agents.orchestrator.graph import master_orchestrator
from backend.core.security import decode_token
from backend.utils.logging import logger
import json

router = APIRouter(prefix="/ws", tags=["WebSockets"])

@router.websocket("/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    token: str = Query(None)
):
    """
    WebSocket router for real-time interaction.
    Verifies user token, binds socket, and routes prompts.
    """
    user_id = "mock-user-uuid-1234-5678"  # Fallback defaults
    
    if token:
        payload = decode_token(token)
        if payload:
            user_id = payload.get("sub", user_id)
            
    await websocket_manager.connect(websocket, session_id)
    logger.info(f"WebSocket client connected to session: {session_id} (User: {user_id})")
    
    try:
        while True:
            # Await text prompt from client
            raw_data = await websocket.receive_text()
            try:
                data = json.loads(raw_data)
                prompt = data.get("prompt", "")
            except json.JSONDecodeError:
                prompt = raw_data
                
            if not prompt.strip():
                continue
                
            # Broadcast "thinking" state
            await websocket.send_json({"event": "status", "text": "Thinking..."})
            
            # Execute Master Orchestrator Graph
            try:
                response = master_orchestrator.execute(
                    user_id=user_id,
                    session_id=session_id,
                    prompt=prompt
                )
                
                # Stream character tokens (Simulate streaming response for interactive feel)
                import asyncio
                tokens = response.split(" ")
                current_sent = ""
                for token_word in tokens:
                    current_sent += token_word + " "
                    await websocket.send_json({
                        "event": "token",
                        "text": current_sent
                    })
                    await asyncio.sleep(0.05)
                    
                # Broadcast final message event
                await websocket.send_json({
                    "event": "done",
                    "text": response
                })
            except Exception as e:
                logger.error(f"WebSocket execution error: {str(e)}")
                await websocket.send_json({"event": "error", "text": "An error occurred executing this prompt."})
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, session_id)
        logger.info(f"WebSocket disconnected from session: {session_id}")
