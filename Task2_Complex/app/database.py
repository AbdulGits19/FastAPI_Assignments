from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Define the databasw
SQLALCHEMY_DATABASE_URL = "sqlite:///./healthcare.db"

# The bridge that connects py code and sql
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 3The transaction, that carries the task
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# parent base
Base = declarative_base()

# This opens a connection when an API hits, and closes it when done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()