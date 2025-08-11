from fastapi import FastAPI
from .db import Base, engine
from . import models
from .api import router as events_router

def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)  # build the warehouse shelves (tables) if missing
    app = FastAPI(title="Mission Events API")
    app.include_router(events_router)
    return app

app = create_app()
