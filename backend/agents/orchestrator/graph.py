from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from backend.agents.orchestrator.state import AgentState
from backend.utils.logging import logger
from backend.core.config import settings

# Placeholder Agents routing
class MasterOrchestrator:
    def __init__(self):
        # Build the graph
        workflow = StateGraph(AgentState)
        
        # Add Nodes
        workflow.add_node("router", self.route_node)
        workflow.add_node("chat_agent", self.chat_node)
        workflow.add_node("notes_agent", self.notes_node)
        workflow.add_node("tasks_agent", self.tasks_node)
        workflow.add_node("documents_agent", self.documents_node)
        workflow.add_node("memory_agent", self.memory_node)
        workflow.add_node("voice_agent", self.voice_node)
        
        # Setup edges
        workflow.set_entry_point("router")
        
        # Routing logic from Router
        workflow.add_conditional_edges(
            "router",
            self.decide_routing,
            {
                "chat_agent": "chat_agent",
                "notes_agent": "notes_agent",
                "tasks_agent": "tasks_agent",
                "documents_agent": "documents_agent",
                "memory_agent": "memory_agent",
                "voice_agent": "voice_agent"
            }
        )
        
        # End nodes all redirect to END
        workflow.add_edge("chat_agent", END)
        workflow.add_edge("notes_agent", END)
        workflow.add_edge("tasks_agent", END)
        workflow.add_edge("documents_agent", END)
        workflow.add_edge("memory_agent", END)
        workflow.add_edge("voice_agent", END)
        
        self.app = workflow.compile()

    def route_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Analyzes prompt contents and sets next routing path.
        """
        messages = state.get("messages", [])
        if not messages:
            return {"next_step": "chat_agent"}
            
        user_message = messages[-1].content.lower()
        logger.info(f"MasterOrchestrator routing query: '{user_message}'")
        
        # Semantic mapping heuristics
        if any(w in user_message for w in ["note", "remind me to write", "memo"]):
            next_step = "notes_agent"
        elif any(w in user_message for w in ["task", "todo", "deadline", "schedule task"]):
            next_step = "tasks_agent"
        elif any(w in user_message for w in ["search pdf", "document", "file", "rag", "read paper"]):
            next_step = "documents_agent"
        elif any(w in user_message for w in ["remember", "memory", "recall", "what did you say about"]):
            next_step = "memory_agent"
        elif any(w in user_message for w in ["voice", "speak", "audio", "transcript"]):
            next_step = "voice_agent"
        else:
            next_step = "chat_agent"
            
        return {"next_step": next_step}

    def decide_routing(self, state: AgentState) -> str:
        return state["next_step"]

    # Nodes Implementations (delegating to separate domain agents)
    def chat_node(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Executing Chat Agent Node")
        # Direct fallback chat response via LangChain / mock API
        from backend.agents.chat.services import chat_agent_service
        resp = chat_agent_service.process_chat(state["messages"][-1].content, state["user_id"])
        return {"response": resp, "messages": [AIMessage(content=resp)]}

    def notes_node(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Executing Notes Agent Node")
        from backend.agents.notes.services import notes_agent_service
        resp = notes_agent_service.process_note_intent(state["messages"][-1].content, state["user_id"])
        return {"response": resp, "messages": [AIMessage(content=resp)]}

    def tasks_node(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Executing Tasks Agent Node")
        from backend.agents.tasks.services import tasks_agent_service
        resp = tasks_agent_service.process_task_intent(state["messages"][-1].content, state["user_id"])
        return {"response": resp, "messages": [AIMessage(content=resp)]}

    def documents_node(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Executing Documents Agent Node")
        from backend.agents.documents.services import document_agent_service
        resp = document_agent_service.process_document_query(state["messages"][-1].content, state["user_id"])
        return {"response": resp, "messages": [AIMessage(content=resp)]}

    def memory_node(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Executing Memory Agent Node")
        from backend.agents.memory.services import memory_agent_service
        resp = memory_agent_service.process_memory_query(state["messages"][-1].content, state["user_id"])
        return {"response": resp, "messages": [AIMessage(content=resp)]}

    def voice_node(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Executing Voice Agent Node")
        from backend.agents.voice.services import voice_agent_service
        resp = voice_agent_service.process_voice_intent(state["messages"][-1].content, state["user_id"])
        return {"response": resp, "messages": [AIMessage(content=resp)]}

    def execute(self, user_id: str, session_id: str, prompt: str) -> str:
        """
        Executes the LangGraph master orchestrator.
        """
        initial_state = {
            "messages": [HumanMessage(content=prompt)],
            "user_id": user_id,
            "session_id": session_id,
            "next_step": "router",
            "response": "",
            "context": {}
        }
        
        output = self.app.invoke(initial_state)
        return output["response"]

master_orchestrator = MasterOrchestrator()
