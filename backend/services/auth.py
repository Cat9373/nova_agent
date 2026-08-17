from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.database.models import User
from backend.core.security import decode_token, verify_password
from backend.repositories.user import user_repository
from backend.utils.logging import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)

class AuthService:
    def authenticate_user(self, db: Session, email: str, plain_password: str) -> User:
        """
        Authenticates a user against local hashed credentials.
        """
        user = user_repository.get_by_email(db, email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        if not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User credentials only managed externally (Supabase)"
            )
        if not verify_password(plain_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        return user

    def verify_token_and_get_user(self, db: Session, token: str) -> User:
        """
        Verifies the JWT token structure and retrieves the User object from database.
        Registers the user in local DB if validated via Supabase but missing locally.
        """
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
            
        payload = decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials or expired session"
            )
            
        # extract user ID and email
        user_id: str = payload.get("sub")
        email: str = payload.get("email") or payload.get("sub") # Fallback to sub if email metadata not in claim
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims"
            )
            
        user = user_repository.get(db, id=user_id)
        if not user:
            # User authenticated externally (e.g. Supabase Auth) but not in local DB yet. Sync user.
            logger.info(f"Syncing external authenticated user locally: {email}")
            user = User(id=user_id, email=email, is_active=True)
            db.add(user)
            db.commit()
            db.refresh(user)
            
        return user

auth_service = AuthService()

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    FastAPI dependency injection to validate incoming request context.
    """
    if not token:
        # Fallback to a development mock user if credentials aren't enforced
        mock_user = db.query(User).filter(User.email == "mock.user@novaagent.ai").first()
        if not mock_user:
            mock_user = User(
                id="mock-user-uuid-1234-5678",
                email="mock.user@novaagent.ai",
                is_active=True
            )
            db.add(mock_user)
            db.commit()
            db.refresh(mock_user)
        return mock_user
        
    return auth_service.verify_token_and_get_user(db, token)
