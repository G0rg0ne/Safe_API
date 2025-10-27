from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite database file
# Create data directory if it doesn't exist
data_dir = os.getenv("DATA_DIR", "/app/data")
os.makedirs(data_dir, exist_ok=True)

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{data_dir}/api_keys.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

