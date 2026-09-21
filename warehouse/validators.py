def validate_bus_performance(performance):

    required_fields = [
        "bus_id",
        "event_count",
        "average_speed",
        "minimum_speed",
        "maximum_speed"
    ]

    for field in required_fields:

        if field not in performance:
            raise ValueError(f"Missing required field: {field}")

    if not performance["bus_id"]:
        raise ValueError("bus_id cannot be empty")

    if performance["event_count"] <= 0:
        raise ValueError("event_count must be greater than zero")

    if performance["minimum_speed"] < 0:
        raise ValueError("minimum_speed cannot be negative")

    if performance["maximum_speed"] > 150:
        raise ValueError("maximum_speed cannot exceed 150")

    if performance["minimum_speed"] > performance["maximum_speed"]:
        raise ValueError("minimum_speed cannot be greater than maximum_speed")

    return True