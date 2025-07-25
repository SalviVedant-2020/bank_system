from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Create SQLite DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./bank.db"

# Engine and session setup
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# This is the missing function!
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
