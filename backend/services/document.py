import io
from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
from backend.database.models import Document
from backend.repositories.document import document_repository
from backend.rag.document_parser.pdf import PDFParser
from backend.rag.chunking.splitter import TextSplitter
from backend.rag.embeddings.service import embedding_service
from backend.services.memory import memory_service
from backend.storage.local import LocalStorage
from backend.storage.supabase import SupabaseStorage
from backend.core.config import settings
from backend.utils.logging import logger

class DocumentService:
    def __init__(self):
        if settings.STORAGE_PROVIDER == "supabase":
            self.storage = SupabaseStorage()
        else:
            self.storage = LocalStorage()
        self.splitter = TextSplitter()

    def get_user_documents(self, db: Session, *, user_id: str) -> List[Document]:
        return document_repository.get_by_user(db, user_id=user_id)

    def get_document(self, db: Session, *, doc_id: str, user_id: str) -> Optional[Document]:
        doc = document_repository.get(db, id=doc_id)
        if doc and doc.user_id == user_id:
            return doc
        return None

    def upload_and_process_document(self, db: Session, *, user_id: str, upload_file: UploadFile) -> Document:
        """
        Flow:
        1. Uploads file to configured Storage Engine.
        2. Saves Document metadata in Postgres DB.
        3. Parses text from File.
        4. Chunks text.
        5. Computes vector embeddings.
        6. Persists embeddings in DB.
        7. Triggers Long term memory record for this document.
        """
        logger.info(f"Uploading file: {upload_file.filename} for user {user_id}")
        
        # Read contents for parser before uploading since upload might consume stream depending on implementation
        contents = upload_file.file.read()
        file_size = len(contents)
        
        # Upload
        file_stream = io.BytesIO(contents)
        file_path = self.storage.upload_file(file_stream, upload_file.filename, folder="documents")
        
        # Create doc record
        doc = Document(
            user_id=user_id,
            file_name=upload_file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=upload_file.content_type or "application/octet-stream",
            storage_provider=settings.STORAGE_PROVIDER
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        # Process and Extract Text
        file_stream_parse = io.BytesIO(contents)
        text_content = PDFParser.extract_text(file_stream_parse, upload_file.filename)
        
        if text_content:
            # Chunking
            chunks = self.splitter.split_text(text_content)
            logger.info(f"Document split into {len(chunks)} chunks.")
            
            # Embeddings
            for idx, chunk in enumerate(chunks):
                # Only process if chunk is not empty
                if chunk.strip():
                    try:
                        vector = embedding_service.get_embedding(chunk)
                        document_repository.create_embedding(
                            db,
                            doc_id=doc.id,
                            chunk_index=idx,
                            text_content=chunk,
                            embedding=vector
                        )
                    except Exception as e:
                        logger.error(f"Failed to embed chunk {idx} for doc {doc.id}: {str(e)}")
            
            # 7. Sync Long Term Memory metadata
            summary_snippet = text_content[:500] + "..." if len(text_content) > 500 else text_content
            memory_content = f"Uploaded document '{doc.file_name}' (size: {doc.file_size} bytes). Preview: {summary_snippet}"
            memory_service.add_memory(
                db, 
                user_id=user_id, 
                category="document", 
                source_id=doc.id, 
                content=memory_content
            )
            
        return doc

    def delete_document(self, db: Session, *, doc_id: str, user_id: str) -> bool:
        doc = self.get_document(db, doc_id=doc_id, user_id=user_id)
        if not doc:
            return False
            
        # Delete from storage
        self.storage.delete_file(doc.file_path)
        
        # Repository remove (handles cascade delete-orphan on embeddings)
        document_repository.remove(db, id=doc_id)
        
        # Remove from memory index
        memory_service.delete_memory_by_source(db, user_id=user_id, source_id=doc_id, category="document")
        return True

document_service = DocumentService()
