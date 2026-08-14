
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from ingestion.main import app
from pathlib import Path
import json

client = TestClient(app)

event_request = {
        "event_type": "gps",
        "source": "gps-simulator",
        "payload": {
            "bus_id": "B101",
            "speed":43.2
        }}


def create_event():

    return client.post("/events", json=event_request)

def get_event_file(event_id: str) -> Path:

    today = datetime.utcnow()

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

    assert stored_event["event_ttype"] == event_request["event_type"]
    assert stored_event["source"] == event_request["source"]
    assert stored_event["payload"] == event_request["payload"]

    assert "event_id" in stored_event
    assert "received_at" in stored_event