from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)  # Optional name for the key
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    
    def is_expired(self):
        """Check if the API key has expired"""
        from datetime import datetime
        return datetime.utcnow() >= self.expires_at
    
    def __repr__(self):
        return f"<APIKey(key='{self.key[:10]}...', expires_at={self.expires_at})>"

