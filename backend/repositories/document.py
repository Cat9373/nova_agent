from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from backend.database.models import Document, DocumentEmbedding
from backend.repositories.base import BaseRepository
from backend.utils.logging import logger

class DocumentRepository(BaseRepository[Document]):
    def get_by_user(self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100) -> List[Document]:
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()

    def create_embedding(self, db: Session, *, doc_id: str, chunk_index: int, text_content: str, embedding: List[float]) -> DocumentEmbedding:
        db_obj = DocumentEmbedding(
            document_id=doc_id,
            chunk_index=chunk_index,
            text_content=text_content,
            embedding=embedding
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def search_embeddings(
        self,
        db: Session,
        *,
        user_id: str,
        query_embedding: List[float],
        document_ids: Optional[List[str]] = None,
        limit: int = 4
    ) -> List[DocumentEmbedding]:
        """
        Retrieves matching document chunks by semantic search using pgvector.
        Limits lookup to specified document_ids if provided, otherwise matches all user documents.
        """
        try:
            query = db.query(DocumentEmbedding).join(Document, DocumentEmbedding.document_id == Document.id).filter(
                Document.user_id == user_id
            )
            if document_ids:
                query = query.filter(Document.id.in_(document_ids))
                
            return query.order_by(DocumentEmbedding.embedding.cosine_distance(query_embedding)).limit(limit).all()
        except Exception as e:
            logger.error(f"pgvector document search failed: {str(e)}. Falling back to default text retrieve.")
            query = db.query(DocumentEmbedding).join(Document, DocumentEmbedding.document_id == Document.id).filter(
                Document.user_id == user_id
            )
            if document_ids:
                query = query.filter(Document.id.in_(document_ids))
            return query.limit(limit).all()

document_repository = DocumentRepository(Document)
