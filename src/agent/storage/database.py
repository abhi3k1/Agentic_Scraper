from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from typing import Any
from ..config import settings

Base = declarative_base()


class ExtractedData(Base):
    __tablename__ = "extracted_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text, nullable=False)
    data = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def save_extraction(url: str, data: Any) -> int:
    s = SessionLocal()
    try:
        entry = ExtractedData(url=url, data=str(data))
        s.add(entry)
        s.commit()
        s.refresh(entry)
        return entry.id
    finally:
        s.close()
