from transformations.pipeline import EventPipeline
from storage.silver import SilverStorage
from storage.quarantine import QuarantineStorage


def test_valid_event_is_processed(tmp_path):

    pipeline = EventPipeline(
        silver_storage=SilverStorage(base_path=tmp_path / "silver"),
        quarantine_storage=QuarantineStorage(base_path=tmp_path / "quarantine"))

    event = {
        "event_id": "123",
        "received_at": "2026-08-14T10:00:00+00:00",
        "event_type": "gps",
        "source": "gps-simulator",
        "payload": {
            "bus_id": " B101 ",
            "speed": "43.2"
        }
    }

    result = pipeline.process(event)
   

    assert result["status"] == "processed"
   

def test_invalid_event_is_quarantined(tmp_path):

    pipeline = EventPipeline(
        silver_storage=SilverStorage(base_path=tmp_path / "silver"),
        quarantine_storage=QuarantineStorage(base_path=tmp_path / "quarantine")
    )

    event = {
        "event_id": "456",
        "received_at": "2026-08-14T10:00:00+00:00",
        "event_type": "gps",
        "source": "gps-simulator",
        "payload": {
            "bus_id": "B101",
            "speed": -20
        }
    }

    result = pipeline.process(event)



    assert result["status"] == "quarantined"
    assert result["reason"] == "speed cannot be negative"
    