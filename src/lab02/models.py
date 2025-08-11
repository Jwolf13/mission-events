from sqlalchemy import Column, Integer, String
from .db import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    details = Column(String, nullable=True)
