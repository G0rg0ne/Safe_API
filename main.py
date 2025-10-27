import uvicorn
from fastapi import FastAPI, Header, Depends, HTTPException, status
from typing import Optional
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
import os
from database import engine, get_db
from models import Base, APIKey
from auth import generate_api_key, create_api_key, require_api_key, verify_api_key
from datetime import datetime, timedelta
from pydantic import BaseModel

# Create database tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: nothing special needed

app = FastAPI(title="Safe API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["138.201.89.207"]
)

# Pydantic models for API key generation
class APIKeyCreate(BaseModel):
    name: Optional[str] = None
    expiration_days: int = 7

class APIKeyResponse(BaseModel):
    key: str
    name: Optional[str]
    created_at: datetime
    expires_at: datetime

# Protected endpoints - require API key
@app.get("/ping")
async def ping(api_key: str = Depends(require_api_key)):
    return {"message": "pong"}

@app.get("/answer-header")
async def answer_from_header(
    message: Optional[str] = Header(None),
    api_key: str = Depends(require_api_key)
):
    if message == "Hello":
        return {"message": "I'am a safe API"}
    else:
        return {"message": "Wrong request"}

@app.get("/health")
async def health(api_key: str = Depends(require_api_key)):
    return {"status": "healthy"}

# Admin endpoints for API key management
@app.post("/admin/create-key", response_model=APIKeyResponse)
async def create_new_api_key(
    key_data: APIKeyCreate,
    db: Session = Depends(get_db)
):
    """Create a new API key with optional name and expiration days (default: 7 days)"""
    api_key = create_api_key(
        db=db,
        name=key_data.name,
        expiration_days=key_data.expiration_days
    )
    return APIKeyResponse(
        key=api_key.key,
        name=api_key.name,
        created_at=api_key.created_at,
        expires_at=api_key.expires_at
    )

@app.get("/admin/list-keys")
async def list_api_keys(db: Session = Depends(get_db)):
    """List all API keys (excluding the actual key values for security)"""
    keys = db.query(APIKey).all()
    return [
        {
            "id": key.id,
            "name": key.name,
            "created_at": key.created_at,
            "expires_at": key.expires_at,
            "is_active": key.is_active,
            "is_expired": key.is_expired()
        }
        for key in keys
    ]

@app.post("/admin/deactivate-key/{key_id}")
async def deactivate_api_key(key_id: int, db: Session = Depends(get_db)):
    """Deactivate an API key"""
    key = db.query(APIKey).filter(APIKey.id == key_id).first()
    if not key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    key.is_active = False
    db.commit()
    return {"message": f"API key {key_id} has been deactivated"}

@app.post("/admin/activate-key/{key_id}")
async def activate_api_key(key_id: int, db: Session = Depends(get_db)):
    """Activate an API key"""
    key = db.query(APIKey).filter(APIKey.id == key_id).first()
    if not key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    key.is_active = True
    db.commit()
    return {"message": f"API key {key_id} has been activated"}

if __name__ == "__main__":
    # Production settings
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=443,
        ssl_keyfile=os.getenv("SSL_KEYFILE", "/app/certs/key.pem"),
        ssl_certfile=os.getenv("SSL_CERTFILE", "/app/certs/cert.pem"),
        workers=4,  # Multiple workers for production
        log_level="info",
        access_log=True
    )