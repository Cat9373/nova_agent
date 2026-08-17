from backend.core.config import settings
from backend.utils.logging import logger

class ChatAgentService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        self.model_name = settings.LLM_MODEL
        self._llm = None
        
        if self.provider == "openai":
            try:
                from langchain_openai import ChatOpenAI
                self._llm = ChatOpenAI(
                    model=self.model_name,
                    openai_api_key=settings.OPENAI_API_KEY
                )
            except ImportError:
                logger.error("langchain_openai package imports failed.")
        elif self.provider == "ollama":
            try:
                from langchain_community.chat_models import ChatOllama
                self._llm = ChatOllama(
                    base_url=settings.OLLAMA_BASE_URL,
                    model=self.model_name
                )
            except ImportError:
                logger.error("langchain_community.chat_models package imports failed.")

    def process_chat(self, prompt: str, user_id: str) -> str:
        """
        Executes a prompt completion with the configured LLM provider.
        """
        if not self._llm or self.provider == "mock":
            logger.info("Executing Chat agent with mock response.")
            return f"Hi! I am NovaAgent. You asked: '{prompt}'. This is a mock response because no LLM provider is active."

        try:
            from langchain_core.messages import HumanMessage
            logger.info(f"Invoking {self.provider} model '{self.model_name}'")
            response = self._llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            logger.error(f"LLM invoke failed: {str(e)}. Falling back to mock reply.")
            return f"NovaAgent Fallback Response: Received your query '{prompt}' but encountered an error processing it with {self.provider}."

chat_agent_service = ChatAgentService()
