from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from models import APIKey
from database import get_db
from datetime import datetime, timedelta
import secrets
import string

def generate_api_key(length=32):
    """Generate a random API key"""
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return key

def create_api_key(db: Session, name: str = None, expiration_days: int = 7):
    """Create a new API key with expiration"""
    key = generate_api_key()
    expires_at = datetime.utcnow() + timedelta(days=expiration_days)
    
    db_key = APIKey(
        key=key,
        name=name,
        expires_at=expires_at
    )
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return db_key

def verify_api_key(api_key: str, db: Session) -> bool:
    """Verify if an API key is valid and not expired"""
    key_record = db.query(APIKey).filter(APIKey.key == api_key).first()
    
    if not key_record:
        return False
    
    if not key_record.is_active:
        return False
    
    if key_record.is_expired():
        return False
    
    return True

def get_api_key_from_header(api_key: str = Header(None), db: Session = Depends(get_db)) -> str:
    """Dependency to extract and validate API key from headers"""
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required. Please provide 'api-key' header.",
        )
    
    if not verify_api_key(api_key, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key.",
        )
    
    return api_key

def require_api_key(api_key: str = Header(None, alias="api-key"), db: Session = Depends(get_db)):
    """Dependency to require API key on protected routes"""
    return get_api_key_from_header(api_key, db)

