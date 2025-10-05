from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import sqlite3
import json
import traceback

# ============================================
# CONFIGURATION
# ============================================
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password hashing
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

# Router
router = APIRouter(prefix="/api/auth", tags=["authentication"])

# ============================================
# DATABASE SETUP
# ============================================
def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('datasage_users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name TEXT,
            created_at TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            last_login TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on import
init_db()

# ============================================
# MODELS
# ============================================
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True

# ============================================
# UTILITY FUNCTIONS
# ============================================
def verify_password(plain_password, hashed_password):
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hash password safely - handle bcrypt limitation"""
    try:
        # Truncate to 72 characters to avoid bcrypt error
        safe_password = str(password)[:72]
        return pwd_context.hash(safe_password)
    except Exception as e:
        print(f"❌ Hashing error: {e}")
        # Fallback to simple SHA256 for development
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()



def get_user_by_username(username: str):
    """Get user from database by username"""
    conn = sqlite3.connect('datasage_users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None

def get_user_by_email(email: str):
    """Get user from database by email"""
    conn = sqlite3.connect('datasage_users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None

def create_user(username: str, email: str, hashed_password: str, full_name: str = None):
    """Create new user in database"""
    conn = sqlite3.connect('datasage_users.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (username, email, hashed_password, full_name, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, hashed_password, full_name, datetime.utcnow().isoformat()))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return user_id
    except sqlite3.IntegrityError as e:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

def authenticate_user(username: str, password: str):
    """Authenticate user credentials"""
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user

def update_last_login(username: str):
    """Update user's last login time"""
    conn = sqlite3.connect('datasage_users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users SET last_login = ? WHERE username = ?
    ''', (datetime.utcnow().isoformat(), username))
    
    conn.commit()
    conn.close()

# ============================================
# API ENDPOINTS
# ============================================
@router.post("/register")
async def register(user: UserRegister):
    """Register new user"""
    try:
        print(f"📝 Registration attempt: {user.username}")
        
        # Check if username exists
        if get_user_by_username(user.username):
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Check if email exists  
        if get_user_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password (truncate to avoid bcrypt 72-byte limit)
        safe_password = str(user.password)[:72]
        hashed_password = get_password_hash(safe_password)
        
        print(f"✅ Password hashed successfully")
        
        # Create user
        user_id = create_user(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name
        )
        
        print(f"✅ User created with ID: {user_id}")
        
        return {
            "success": True,
            "message": "User registered successfully",
            "user_id": user_id,
            "username": user.username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")



@router.post("/login")
async def login(user: UserLogin):
    """Login user"""
    # Authenticate user
    db_user = authenticate_user(user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    # Update last login
    update_last_login(user.username)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user['username']},
        expires_delta=access_token_expires
    )
    
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user['id'],
            "username": db_user['username'],
            "email": db_user['email'],
            "full_name": db_user['full_name']
        }
    }

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current logged-in user info"""
    return {
        "id": current_user['id'],
        "username": current_user['username'],
        "email": current_user['email'],
        "full_name": current_user['full_name'],
        "created_at": current_user['created_at'],
        "last_login": current_user['last_login']
    }

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout user (client should delete token)"""
    return {
        "success": True,
        "message": "Logged out successfully"
    }

@router.post("/verify-token")
async def verify_token(current_user: dict = Depends(get_current_user)):
    """Verify if token is valid"""
    return {
        "valid": True,
        "username": current_user['username']
    }
