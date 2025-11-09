from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

# Pydantic models for request/response
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True

@router.post("/register", response_model=dict)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        db_user = UserService.create_user(
            db=db,
            username=user.username,
            email=user.email,
            password=user.password
        )
        # FIXED RESPONSE FORMAT
        return {
            "success": True,                    
            "message": "User created successfully",
            "user": {                          
                "id": db_user.id,
                "username": db_user.username,
                "email": db_user.email,
                "is_active": db_user.is_active,
                "created_at": db_user.created_at.isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=dict)  
async def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    user = UserService.authenticate_user(
        db, user_credentials.username, user_credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = AuthService.create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    # ✅ FIXED RESPONSE FORMAT
    return {
        "success": True,                        
        "access_token": access_token,
        "token": access_token,                  
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat()
        }
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    current_user = AuthService.get_current_user(db, token.credentials)
    return current_user

@router.get("/verify-token")
async def verify_token(token: str = Depends(security)):
    """Verify if token is valid"""
    try:
        payload = AuthService.verify_token(token.credentials)
        return {"valid": True, "username": payload["username"]}
    except HTTPException:
        return {"valid": False}


@router.post("/logout", response_model=dict)
async def logout():
    """Stateless logout endpoint for JWT-based auth"""
    # With JWT, logout is handled client-side by discarding the token
    return {"success": True, "message": "Logged out"}