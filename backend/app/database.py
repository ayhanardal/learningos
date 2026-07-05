import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Docker-compose içindeki DATABASE_URL ortam değişkenini al
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://learningos_user:supersecretpassword@db:5432/learningos_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
