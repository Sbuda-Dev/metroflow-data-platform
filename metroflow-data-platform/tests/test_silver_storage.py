import json
from storage.silver import SilverStorage


def test_event_is_saved_to_silver(tmp_path):

    storage = SilverStorage(base_path=tmp_path)

    event = {
        "event_id": "123",
        "received_at": "2026-08-14T10:00:00+00:00",
        "bus_id": "B101",
        "speed": 43.2
    }

    storage.save(event)

    files = list(tmp_path.rglob("*.json"))

    assert len(files) == 1

def test_saved_silver_event_is_correct(tmp_path):

    storage = SilverStorage(base_path=tmp_path)

    event = {
            "event_id": "123",
            "received_at": "2026-08-14T10:00:00+00:00",
            "bus_id": "B101",
            "speed": 43.2
        }

    storage.save(event)

    files = list(tmp_path.rglob("*json"))

    with open(files[0]) as file:
        stored_event = json.load(file)

    assert stored_event == event