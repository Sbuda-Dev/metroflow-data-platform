from transformations.gps import transform_gps_event

def test_gps_event_is_transformed():

    bronze_event = {
        "event_id": "123",
        "received_at": "2026-08-14T10:00:00+00:00",
        "event_type": "gps",
        "source": "gps-simulator",
        "payload": {
            "bus_id": " B101 ",
            "speed": "43.2"
        }
    }

    silver_event = transform_gps_event(bronze_event)

    assert silver_event["bus_id"] == "B101"
    assert silver_event["speed"] == 43.2