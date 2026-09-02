from datetime import datetime, timezone
from uuid import uuid4
from storage.bronze import BronzeStorage
from .models import EventRequest
from database.connection import SessionLocal
from database.models import GPSEvent
from database.repositories import GPSEventRepository

storage = BronzeStorage()

class EventService:

    def create_event(self, event: EventRequest):

        event_id = uuid4()
        received_at = datetime.now(timezone.utc)

        stored_event = {
            "event_id": str(event_id),
            "received_at": received_at.isoformat(),
            "event_type": event.event_type,
            "source": event.source,
            "payload": event.payload,
        }

        storage.save(stored_event)

        database_event = GPSEvent(
            event_id=event_id,
            received_at=received_at,
            event_type=event.event_type,
            source=event.source,
            bus_id=event.payload["bus_id"],
            speed=event.payload["speed"]
        )

        session = SessionLocal()

        try:

            repository = GPSEventRepository(session)
            repository.save(database_event)

        finally:

            session.close()

        return stored_event