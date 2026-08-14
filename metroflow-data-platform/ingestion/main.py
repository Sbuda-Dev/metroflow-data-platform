from datetime import datetime, timezone
from uuid import uuid4
from fastapi import FastAPI, status
from .models import EventRequest
from .services import EventService

app = FastAPI(
    title="MetroFlow Data Platform",
    version="1.0.0"
)

service = EventService()

@app.get("/health")
def health():

    return {"status" : "healthy"}

@app.post("/events", status_code=status.HTTP_201_CREATED)
def create_event(event: EventRequest):

    return service.create_event(event)