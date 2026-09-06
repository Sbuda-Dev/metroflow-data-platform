import json

from datetime import datetime, timezone
from fastapi.testclient import TestClient
from ingestion.main import app
from pathlib import Path
from database.connection import SessionLocal
from database.repositories import GPSEventRepository
from uuid import uuid4
from ingestion.models import EventRequest
from ingestion.services import EventService
from storage.bronze import BronzeStorage


client = TestClient(app)

event_request = {
        "event_id": str(uuid4()),
        "event_type": "gps",
        "source": "gps-simulator",
        "payload": {
            "bus_id": "B101",
            "speed":43.2
        }}

def create_event_request():

    return {
        "event_id": str(uuid4()),
        "event_type": "gps",
        "source": "gps-simulator",
        "payload": {
            "bus_id": "B101",
            "speed": 43.2
        }
    } 


def create_event():

    event_request = create_event_request()

    return client.post("/events", json=event_request)

def get_event_file(event_id: str) -> Path:

    today = datetime.now(timezone.utc)

    return (
        Path("data") 
        / "bronze" 
        / f"year={today.year}" 
        / f"month={today.month:02d}" 
        / f"day={today.day:02d}" 
        / f"{event_id}.json")

def test_event_response_status_returns_201():

    response = create_event()

    assert response.status_code == 201

def test_event_data_response_is_correct():

    response = create_event()
    response_data = response.json()

    assert response_data["event_type"] == event_request["event_type"]
    assert response_data["source"] == event_request["source"]
    assert response_data["payload"]["bus_id"] == event_request["payload"]["bus_id"]
    assert response_data["payload"]["speed"] == event_request["payload"]["speed"]


def test_event_uuid_is_in_data():

    response = create_event()
    response_data = response.json()

    assert "event_id" in response_data

def test_event_speed_in_data():

    response = create_event()
    response_data = response.json()

    assert "speed" in response_data["payload"]

def test_event_is_saved_to_bronze_storage():

    response = create_event()
    response_data = response.json()

    event_id = response_data["event_id"]

    expected_file = (get_event_file(event_id))

    assert expected_file.exists()

def test_saved_event_matches_request():

    response = create_event()
    response_data = response.json()

    event_id = response_data["event_id"]

    expected_file = (get_event_file(event_id))

    stored_event = json.loads(expected_file.read_text())

    assert stored_event["event_type"] == event_request["event_type"]
    assert stored_event["source"] == event_request["source"]
    assert stored_event["payload"] == event_request["payload"]

    assert "event_id" in stored_event
    assert "received_at" in stored_event

def test_event_is_saved_to_database():

    response = create_event()

    assert response.status_code == 201

    response_data = response.json()

    event_id = response_data["event_id"]

    session = SessionLocal()

    try:

        repository = GPSEventRepository(session)

        stored_event = repository.find_by_id(event_id)

        assert stored_event is not None
        assert str(stored_event.event_id) == event_id
        assert stored_event.event_type == event_request["event_type"]
        assert stored_event.source == event_request["source"]
        assert stored_event.bus_id == event_request["payload"]["bus_id"]
        assert float(stored_event.speed) == event_request["payload"]["speed"]

    finally:

        session.close()


def test_duplicate_event_is_not_inserted_twice():

    event_id = str(uuid4())

    request = {
        "event_id": event_id,
        "event_type": "gps",
        "source": "gps-simulator",
        "payload": {
            "bus_id": "B999",
            "speed": 45.0
        }
    }

    first_response = client.post("/events", json=request)
    second_response = client.post("/events", json=request)

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    session = SessionLocal()

    try:

        repository = GPSEventRepository(session)

        stored_event = repository.find_by_id(event_id)

        assert stored_event is not None

    finally:

        session.close()


def test_event_remains_in_bronze_when_database_fails():

    class FailingRepository:

        def __init__(self, session):
            pass

        def save(self, event):
            raise Exception("Database unavailable")


    storage = BronzeStorage()

    failing_service = EventService(storage=storage, repository_factory=FailingRepository)

    event_id = uuid4()

    request = EventRequest(
        event_id=event_id,
        event_type="gps",
        source="gps-simulator",
        payload={
            "bus_id": "B777",
            "speed": 40.0
        }
    )

    try:

        failing_service.create_event(request)

    except Exception:
        pass

    expected_file = get_event_file(str(event_id))

    assert expected_file.exists()




















