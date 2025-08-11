from pydantic import BaseModel

class EventBase(BaseModel):
    title: str
    details: str | None = None

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: int
    class Config:
        from_attributes = True
