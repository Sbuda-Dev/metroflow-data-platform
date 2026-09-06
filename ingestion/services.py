from datetime import datetime, timezone
from storage.bronze import BronzeStorage
from .models import EventRequest
from database.connection import SessionLocal
from database.models import GPSEvent
from database.repositories import GPSEventRepository



class EventService:

    def __init__(self, storage=None, repository_factory=None, session_factory=SessionLocal):

        self.storage = storage or BronzeStorage()
        self.repository_factory = repository_factory or GPSEventRepository
        self.session_factory = session_factory

    def create_event(self, event: EventRequest):

        event_id = event.event_id
        received_at = datetime.now(timezone.utc)

        stored_event = {
            "event_id": str(event_id),
            "received_at": received_at.isoformat(),
            "event_type": event.event_type,
            "source": event.source,
            "payload": event.payload,
        }

        self.storage.save(stored_event)

        database_event = GPSEvent(
            event_id=event_id,
            received_at=received_at,
            event_type=event.event_type,
            source=event.source,
            bus_id=event.payload["bus_id"],
            speed=event.payload["speed"]
        )

        session = self.session_factory()

        try:

            repository = self.repository_factory(session)
            repository.save(database_event)

        finally:

            session.close()

        return stored_event