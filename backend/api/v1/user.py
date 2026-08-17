from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.schemas.profile import ProfileResponse, ProfileUpdate
from backend.services.auth import get_current_user
from backend.database.models import User
from backend.services.profile import profile_service

router = APIRouter(prefix="/user", tags=["User Profile"])

@router.get("/profile", response_model=ProfileResponse)
def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns profile information associated with current authenticated user context.
    """
    return profile_service.get_profile(db, user_id=current_user.id)

@router.patch("/profile", response_model=ProfileResponse)
def update_user_profile(
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates profile fields for current authenticated user.
    """
    return profile_service.update_profile(db, user_id=current_user.id, profile_in=payload)
