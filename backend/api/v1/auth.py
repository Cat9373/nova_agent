from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.schemas.auth import LoginRequest, Token
from backend.schemas.user import UserCreate, UserResponse
from backend.services.user import user_service
from backend.services.auth import auth_service
from backend.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Local developer signup route. Registers credentials locally.
    In production, Supabase Auth dashboard handles signup flow.
    """
    user = user_service.get_user_by_email(db, email=payload.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists."
        )
    return user_service.create_user(db, user_in=payload)

@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Local developer login endpoint returning local JWT signature.
    """
    user = auth_service.authenticate_user(db, email=payload.email, plain_password=payload.password)
    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer")
