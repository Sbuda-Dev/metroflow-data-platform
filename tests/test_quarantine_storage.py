import json
from storage.quarantine import QuarantineStorage

def test_invalid_event_is_saved_to_quarantine(tmp_path):

    storage = QuarantineStorage(base_path=tmp_path)

    event = {
        "event_id": "123",
        "received_at": "2026-08-14T10:00:00+00:00",
        "event_type": "gps",
        "source": "gps-simulator",
        "payload": {
            "bus_id": "B101",
            "speed": -20
        }
    }

    storage.save(event, "speed cannot be negative")

    files = list(tmp_path.rglob("*.json"))

    assert len(files) == 1


def test_quarantine_record_contains_reason(tmp_path):

    storage = QuarantineStorage(base_path=tmp_path)

    event = {
        "event_id": "123",
        "received_at": "2026-08-14T10:00:00+00:00",
        "event_type": "gps",
        "source": "gps-simulator",
        "payload":{
            "bus_id": "B101",
            "speed": -20
        }
    }

    reason = "speed cannot be negative"

    storage.save(event, reason)

    files = list(tmp_path.rglob("*.json"))

    with open(files[0]) as file:
        record = json.load(file)

    assert record["event_id"] == "123"
    assert record["reason"] == reason
    assert record["event"] == event