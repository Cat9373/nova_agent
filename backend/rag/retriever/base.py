from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.repositories.document import document_repository
from backend.rag.embeddings.service import embedding_service
from backend.utils.logging import logger

class DocumentRetriever:
    def retrieve_chunks(
        self,
        db: Session,
        *,
        user_id: str,
        query: str,
        document_ids: Optional[List[str]] = None,
        limit: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Calculates user query vector and queries database.
        Returns mapped results matching context format for LLMs.
        """
        logger.info(f"Retrieving chunks for user {user_id} on query: '{query}'")
        query_vector = embedding_service.get_embedding(query)
        
        db_chunks = document_repository.search_embeddings(
            db,
            user_id=user_id,
            query_embedding=query_vector,
            document_ids=document_ids,
            limit=limit
        )
        
        results = []
        for chunk in db_chunks:
            results.append({
                "chunk_index": chunk.chunk_index,
                "text_content": chunk.text_content,
                "document_id": chunk.document_id,
                "file_name": chunk.document.file_name if chunk.document else "Unknown File"
            })
            
        return results

document_retriever = DocumentRetriever()
