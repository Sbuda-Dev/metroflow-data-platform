import pytest
from transformations.validators import validate_gps_event


def test_valid_gps_event_passes_validation():

    event = {
        "payload":{
            "bus_id": "B101",
            "speed": 43.2
        }
    }

    assert validate_gps_event(event) is True

def test_negative_speed_is_rejected():

    event = {
        "payload": {
            "bus_id": "B101",
            "speed": -20
        }
    }

    with pytest.raises(ValueError, match="speed cannot be negative"):

        validate_gps_event(event)

def test_non_numeric_speed_is_rejected():

    event = {
        "payload": {
            "bus_id": "B101",
            "speed": "fast"
        }
    }

    with pytest.raises(ValueError, match="speed must be numeric"):

        validate_gps_event(event)

def test_speed_above_150_is_rejected():

    event = {
        "payload": {
            "bus_id": "B101",
            "speed": 151
        }
    }

    with pytest.raises(ValueError, match="speed cannot exceed 150 km/h"):
        validate_gps_event(event)

def test_missing_bus_id_is_rejected():

    event = {
        "payload": {
            "speed": 43.2
        }
    }

    with pytest.raises(ValueError):
        validate_gps_event(event)

def test_empty_bus_id_is_rejected():

    event = {
        "payload": {
            "bus_id": "",
            "speed": 43.2
        }
    }

    with pytest.raises(ValueError, match="bus_id is required"):
        validate_gps_event(event)

