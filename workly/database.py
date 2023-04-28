import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./workly.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
