from sqlalchemy.orm import Session
from backend.database.session import SessionLocal
from backend.rag.retriever.base import document_retriever
from backend.utils.logging import logger

class DocumentAgentService:
    def process_document_query(self, prompt: str, user_id: str) -> str:
        """
        Retrieves matching document segments (RAG) and builds the LLM response context.
        """
        logger.info(f"DocumentAgent RAG processing: '{prompt}'")
        db: Session = SessionLocal()
        try:
            # Retrieve relevant chunks from uploaded PDFs
            chunks = document_retriever.retrieve_chunks(
                db, 
                user_id=user_id, 
                query=prompt, 
                limit=3
            )
            
            if not chunks:
                return "I couldn't find any relevant details in your uploaded documents. Make sure you upload a PDF file first."
                
            # Compile context
            context_str = ""
            for idx, chunk in enumerate(chunks, 1):
                context_str += f"Source ({chunk['file_name']}): {chunk['text_content']}\n\n"
                
            # Synthesize final answer mock / response
            response = (
                f"Based on your documents, here is what I found:\n\n"
                f"{context_str}\n"
                f"Hope this answers your query regarding '{prompt}'!"
            )
            return response
        finally:
            db.close()

document_agent_service = DocumentAgentService()
