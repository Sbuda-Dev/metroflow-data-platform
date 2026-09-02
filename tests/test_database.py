from sqlalchemy import text
from database.connection import engine, SessionLocal
from database.repositories import GPSEventRepository
from database.models import GPSEvent
from datetime import datetime, timezone
from uuid import uuid4

def test_database_connection():

    with engine.connect() as connection:

        result = connection.execute(text("SELECT 1"))

        assert result.scalar() == 1

def test_can_create_gps_event_object():

    event = GPSEvent(
        event_id=uuid4(),
        received_at=datetime.now(timezone.utc),
        event_type="gps",
        source="gps-simulator",
        bus_id="B101",
        speed=43.2
    )

    assert event.event_type == "gps"
    assert event.source == "gps-simulator"
    assert event.bus_id == "B101"
    assert event.speed == 43.2

def test_can_save_gps_event():

    event_id = uuid4()

    event = GPSEvent(
         event_id=event_id,
        received_at=datetime.now(timezone.utc),
        event_type="gps",
        source="gps-simulator",
        bus_id="B999",
        speed=55.5
    )

    session = SessionLocal()

    try:
        session.add(event)
        session.commit()

        stored_event = session.get(GPSEvent, event_id)

        assert stored_event is not None
        assert stored_event.event_id == event_id
        assert stored_event.bus_id == "B999"
        assert float(stored_event.speed) == 55.5

    finally:

        session.close()

def test_repository_can_save_event():

    event_id = uuid4()

    event = GPSEvent(
        event_id=event_id,
        received_at=datetime.now(timezone.utc),
        event_type="gps",
        source="gps-simulator",
        bus_id="B101",
        speed=43.2
    )

    session = SessionLocal()
    

    try:

        repository = GPSEventRepository(session)
        repository.save(event)

        stored_event = repository.find_by_id(event_id)

        assert stored_event is not None
        assert stored_event.bus_id == "B101"
        assert float(stored_event.speed) == 43.2

    finally:
        session.close()

def test_duplicate_event_is_not_inserted_twice():

    event_id = uuid4()

    event = GPSEvent(
        event_id=event_id,
        received_at=datetime.now(timezone.utc),
        event_type="gps",
        source="gps-simulator",
        bus_id="B555",
        speed=45.0
    )

    session = SessionLocal()

    try:

        repository = GPSEventRepository(session)
        first_insert = repository.save(event)

        duplicate = GPSEvent(
            event_id=event_id,
            received_at=datetime.now(timezone.utc),
            event_type="gps",
            source="gps-simulator",
            bus_id="B555",
            speed=99.0
        )

        second_insert = repository.save(duplicate)

        assert first_insert is True
        assert second_insert is False

        
    finally:

        session.close()
