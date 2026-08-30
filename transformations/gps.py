from .validators import validate_gps_event

def transform_gps_event(event):

    validate_gps_event(event)

    return{
        "event_id": event["event_id"],
        "received_at": event["received_at"],
        "bus_id": event["payload"]["bus_id"].strip(),
        "speed": float(event["payload"]["speed"]),
    }