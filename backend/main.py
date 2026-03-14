from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.database import init_db
from backend.routes.incidents import router as incidents_router

app = FastAPI(title="SafeIncident")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(incidents_router)


@app.on_event("startup")
def on_startup():
    init_db()
