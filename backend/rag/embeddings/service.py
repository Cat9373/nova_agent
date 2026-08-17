from typing import List
import random
from backend.core.config import settings
from backend.utils.logging import logger

class EmbeddingService:
    def __init__(self):
        self.provider = settings.EMBEDDING_PROVIDER.lower()
        self.model = settings.EMBEDDING_MODEL
        self._client = None
        
        if self.provider == "openai":
            try:
                from langchain_openai import OpenAIEmbeddings
                self._client = OpenAIEmbeddings(
                    model=self.model,
                    api_key=settings.OPENAI_API_KEY
                )
            except ImportError:
                logger.error("Failed to import langchain_openai. Ensure requirements are met.")
        elif self.provider == "ollama":
            try:
                from langchain_community.embeddings import OllamaEmbeddings
                self._client = OllamaEmbeddings(
                    base_url=settings.OLLAMA_BASE_URL,
                    model=self.model
                )
            except ImportError:
                logger.error("Failed to import OllamaEmbeddings from langchain_community.")

    def get_embedding(self, text: str) -> List[float]:
        """
        Generates a 1536-dimensional float vector for a given text.
        """
        if self.provider == "mock" or not self._client:
            # Generate deterministic mock vector of dimension 1536
            random.seed(hash(text))
            vector = [random.uniform(-1.0, 1.0) for _ in range(1536)]
            # Normalize vector
            norm = sum(x*x for x in vector) ** 0.5
            return [x / norm for x in vector]
            
        try:
            return self._client.embed_query(text)
        except Exception as e:
            logger.error(f"Embedding generation failed via {self.provider}: {str(e)}. Falling back to mock embedding.")
            # Fallback
            random.seed(hash(text))
            vector = [random.uniform(-1.0, 1.0) for _ in range(1536)]
            norm = sum(x*x for x in vector) ** 0.5
            return [x / norm for x in vector]

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        if self.provider == "mock" or not self._client:
            return [self.get_embedding(t) for t in texts]
        try:
            return self._client.embed_documents(texts)
        except Exception as e:
            logger.error(f"Batch embedding generation failed: {str(e)}")
            return [self.get_embedding(t) for t in texts]

embedding_service = EmbeddingService()
