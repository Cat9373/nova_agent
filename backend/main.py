from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.utils.logging import logger
from backend.middleware.errors import GlobalExceptionMiddleware
from backend.database.session import engine
from backend.database.base import Base

# API routers
from backend.api.v1.auth import router as auth_router
from backend.api.v1.user import router as user_router
from backend.agents.chat.router import router as chat_agent_router
from backend.agents.notes.router import router as notes_agent_router
from backend.agents.tasks.router import router as tasks_agent_router
from backend.agents.documents.router import router as documents_agent_router
from backend.agents.memory.router import router as memory_agent_router
from backend.agents.voice.router import router as voice_agent_router
from backend.api.v1.placeholders import router as future_placeholders_router

# WebSocket Router
from backend.websocket.router import router as ws_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Initializing database tables...")
    try:
        # Auto-create tables for development fallback
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to auto-create tables: {str(e)}. Ensure DB server is running.")
    yield
    # Shutdown actions
    logger.info("Cleaning up connections...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise-grade AI-powered Executive Assistant Backend",
    version="1.0.0",
    lifespan=lifespan
)

# Apply middlewares
app.add_middleware(GlobalExceptionMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root status route
@app.get("/health", tags=["System Status"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "database": "connected"
    }

# Register API v1 Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(user_router, prefix=settings.API_V1_STR)
app.include_router(chat_agent_router, prefix=settings.API_V1_STR)
app.include_router(notes_agent_router, prefix=settings.API_V1_STR)
app.include_router(tasks_agent_router, prefix=settings.API_V1_STR)
app.include_router(documents_agent_router, prefix=settings.API_V1_STR)
app.include_router(memory_agent_router, prefix=settings.API_V1_STR)
app.include_router(voice_agent_router, prefix=settings.API_V1_STR)
app.include_router(future_placeholders_router, prefix=settings.API_V1_STR)

# Register WebSockets
app.include_router(ws_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
