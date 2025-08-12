from pydantic import BaseModel, ConfigDict


# Shared fields used across create/update/read
class EventBase(BaseModel):
    title: str
    details: str | None = None


# Payload for creating a new event
class EventCreate(EventBase):
    pass


# Payload for partial updates (optional fields)
class EventUpdate(BaseModel):
    title: str | None = None
    details: str | None = None


# What we return from the API (includes DB id)
class EventRead(EventBase):
    id: int

    # Pydantic v2 config: allow ORM objects -> schema
    model_config = ConfigDict(from_attributes=True)
