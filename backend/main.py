from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.database import Base, engine
from backend.routes.incidents import router as incidents_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SafeIncident")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(incidents_router)

