from datetime import datetime, timezone
from uuid import uuid4
from storage.bronze import BronzeStorage
from .models import EventRequest

storage = BronzeStorage()

class EventService:

    def create_event(self, event: EventRequest):

        stored_event = {
            "event_id": str(uuid4()),
            "received_at": datetime.now(timezone.utc).isoformat(),
            "event_type": event.event_type,
            "source": event.source,
            "payload": event.payload,
        }

        storage.save(stored_event)

        return stored_event