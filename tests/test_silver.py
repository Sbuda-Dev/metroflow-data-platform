from transformations.silver import SilverTransformer

def test_transform_event_flattens_payload():

    bronze_event = {
        "event_id": "123",
        "received_at": "2026-09-19T10:00:00+00:00",
        "event_type": "gps",
        "source": "gps-simulator",
        "payload": {
            "bus_id": "B101",
            "speed": 43.2
        }
    }

    transformer = SilverTransformer()

    silver_event = transformer.transform_event(bronze_event)

    assert silver_event["event_id"] == "123"
    assert silver_event["event_type"] == "gps"
    assert silver_event["source"] == "gps-simulator"
    assert silver_event["bus_id"] == "B101"
    assert silver_event["speed"] == 43.2

    assert "payload" not in silver_event