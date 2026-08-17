# NovaAgent System Architecture Design Documentation

This document describes the design patterns, databases schemas, multi-agent orchestrator graphs, and setups for the NovaAgent Enterprise AI Assistant.

```
                  ┌─────────────────────────────────────┐
                  │   Desktop / Web / Mobile Clients    │
                  └──────────────────┬──────────────────┘
                                     │ HTTP / WebSockets
                                     ▼
                  ┌─────────────────────────────────────┐
                  │      FastAPI Gateway (Uvicorn)       │
                  └──────────────────┬──────────────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            ▼                        ▼                        ▼
  ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
  │   Auth / JWT     │     │   API Routers    │     │ WebSocket Stream │
  └────────┬─────────┘     └────────┬─────────┘     └────────┬─────────┘
           │                        │                        │
           ▼                        ▼                        ▼
  ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
  │  Supabase Auth   │     │  Service Layers  │     │ Master LangGraph │
  └──────────────────┘     └────────┬─────────┘     └────────┬─────────┘
                                    │                        │
                                    ├────────────────────────┤
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │ Domain Agents Interface │
                       └────────────┬────────────┘
                                    │
       ┌───────────┬────────────┬───┴───────┬────────────┐
       ▼           ▼            ▼           ▼            ▼
   ┌───────┐   ┌───────┐    ┌───────┐   ┌───────┐    ┌───────┐
   │ Notes │   │ Tasks │    │ RAG / │   │ Memory│    │ Voice │
   │ Agent │   │ Agent │    │ Docs  │   │ Agent │    │ Agent │
   └───────┘   └───────┘    └───────┘   └───────┘    └───────┘
```

## System Layers

1. **API Routing**: FastAPI is configured with modular routers under `backend/api/` and `backend/agents/`.
2. **Business Services**: Layer containing core business logic (e.g. `DocumentService`, `NoteService`, `TaskService`) mapping entities to active connections.
3. **Database Repositories**: Implements a clean generic repository pattern (`BaseRepository[T]`) separating ORM statements from services.
4. **AI Orchestrator**: LangGraph handles conversational workflows, routing prompts to specific sub-agents (e.g. RAG, Notes, Tasks) according to heuristics.
5. **Storage Manager**: Supports local filesystem and cloud Supabase Storage bindings.

## Databases Schema Design

NovaAgent utilizes **PostgreSQL** with the **pgvector** extension.

- **User**: Stores login credentials reference.
- **Profile**: Stores name, phone and avatar URL properties.
- **Task**: Stores todos, priorities and status keys.
- **Meeting**: Stores future meeting transcripts and action item extractions.
- **CalendarEvent**: Stores calendar timelines and schedules.
- **Note**: Stores user notes and documentation text.
- **Document**: Metadata for uploaded assets (PDFs, TXT).
- **DocumentEmbedding**: Chunked text snippets paired with **pgvector** vectors.
- **Memory**: Long term memory semantic store storing vector representations of crucial notifications (meetings, actions, deadlines, preferences).

## AI Agent Inferences

Each agent incorporates a service layer executing LLM prompts using **LangChain**:
- Local LLM fallback: Ollama integration.
- Cloud LLM: OpenAI GPT-4.
- Deterministic mock fallback: Handles execution when offline or provider keys are missing.
