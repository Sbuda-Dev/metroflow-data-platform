from transformations.gold import calculate_bus_performance

def test_bus_performance_is_calculated():

    events = [
        {
            "bus_id": "B101",
            "speed": 40.0
        },
        {
            "bus_id": "B101",
            "speed": 50.0
        },
        {
            "bus_id": "B101",
            "speed": 60.0
        },
       
    ]

    result = calculate_bus_performance(events)

    assert result == [{
        "bus_id": "B101",
        "event_count": 3,
        "average_speed": 50.0,
        "minimum_speed": 40.0,
        "maximum_speed": 60.0
    }]

