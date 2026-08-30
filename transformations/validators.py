
def validate_gps_event(event):

    payload = event["payload"]

    bus_id = payload.get("bus_id")
    speed = payload.get("speed")

    if not bus_id:
        raise ValueError("bus_id is required")

    try:
        speed = float(speed)

    except (TypeError, ValueError):
        raise ValueError("speed must be numeric")

    if speed <0:
        raise ValueError("speed cannot be negative")

    if speed > 150:
        raise ValueError("speed cannot exceed 150 km/h")

    return True