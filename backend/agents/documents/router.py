from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from typing import List
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.schemas.documents import DocumentResponse, DocumentChatQuery
from backend.services.auth import get_current_user
from backend.database.models import User
from backend.services.document import document_service
from backend.agents.documents.services import document_agent_service

router = APIRouter(prefix="/documents", tags=["Documents Agent"])

@router.get("", response_model=List[DocumentResponse])
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return document_service.get_user_documents(db, user_id=current_user.id)

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Uploads document (PDF/TXT), extracts text, chunks it, embeds it and triggers
    saving to database for RAG workflows.
    """
    try:
        return document_service.upload_and_process_document(db, user_id=current_user.id, upload_file=file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

@router.post("/chat")
def chat_with_documents(
    payload: DocumentChatQuery,
    current_user: User = Depends(get_current_user)
):
    """
    Performs RAG query against uploaded document embeddings context.
    """
    try:
        return {"response": document_agent_service.process_document_query(payload.query, current_user.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    doc_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = document_service.delete_document(db, doc_id=doc_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return None
