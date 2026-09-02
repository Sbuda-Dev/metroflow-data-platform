from transformations.pipeline import EventPipeline
from storage.silver import SilverStorage
from storage.quarantine import QuarantineStorage
from storage.processed import ProcessedEventStore


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
            "speed": 43.2
        }
    }

    result = pipeline.process(event)
   

    assert result["status"] == "duplicate"
   

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

def test_duplicate_event_is_not_processed_twice(tmp_path):

    pipeline = EventPipeline(silver_storage=SilverStorage(base_path=tmp_path / "silver"), 
                quarantine_storage=QuarantineStorage(base_path=tmp_path / "quarantine"),
                processed_store=ProcessedEventStore(base_path=tmp_path / "processed"))

    event = {
        "event_id": "123",
        "received_at": "2026-08-14T10:00:00+00:00",
        "event_type": "gps",
        "source": "gps-simulator",
        "payload": {
            "bus_id": "B101",
            "speed": 43.2
        }
    }

    first_result = pipeline.process(event)
    second_result = pipeline.process(event)

    assert first_result["status"] == "processed"
    assert second_result["status"] == "duplicate"

        
    