from typing import List, Dict, Any, TypedDict, Annotated
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    user_id: str
    session_id: str
    next_step: str
    response: str
    context: Dict[str, Any]
