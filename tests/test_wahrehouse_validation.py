import pytest

from warehouse.validators import validate_bus_performance

def test_valid_bus_performance():

    performance = {
        "bus_id": "B101",
        "event_count": 3,
        "average_speed": 50.0,
        "minimum_speed": 40.0,
        "maximum_speed": 60.0
    }

    assert validate_bus_performance(performance) is True


def test_bus_performance_requires_bus_id():

    performance = {
        "event_count": 3,
        "average_speed": 50.0,
        "minimum_speed": 40.0,
        "maximum_speed": 60.0
    }

    with pytest.raises(ValueError, match="Missing required field: bus_id"):
        validate_bus_performance(performance)

def test_event_count_must_be_positive():

    performance = {
        "bus_id": "B101",
        "event_count": 0,
        "average_speed": 50.0,
        "minimum_speed": 40.0,
        "maximum_speed": 60.0
    }

    with pytest.raises(ValueError, match="event_count must be greater than zero"):
        validate_bus_performance(performance)

def test_maximum_speed_cannot_exceed_limit():

    performance = {
        "bus_id": "B101",
        "event_count": 3,
        "average_speed": 170.0,
        "minimum_speed": 160.0,
        "maximum_speed": 170.0
    }

    with pytest.raises(ValueError, match="maximum_speed cannot exceed 150"):
        validate_bus_performance(performance)


def test_minimum_speed_cannot_exceed_maximum_speed():

    performance = {
        "bus_id": "B101",
        "event_count": 3,
        "average_speed": 50.0,
        "minimum_speed": 80.0,
        "maximum_speed": 60.0
    }

    with pytest.raises(ValueError, match="minimum_speed cannot be greater than maximum_speed"):
        validate_bus_performance(performance)