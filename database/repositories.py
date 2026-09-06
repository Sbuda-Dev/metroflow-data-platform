from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import GPSEvent
from sqlalchemy.dialects.postgresql import insert

class GPSEventRepository:

    def __init__(self, session: Session):

        self.session = session

    def save(self, event: GPSEvent) -> bool:

        statement = insert(GPSEvent).values(
            event_id=event.event_id,
            received_at=event.received_at,
            event_type=event.event_type,
            source=event.source,
            bus_id=event.bus_id,
            speed=event.speed
        )

        statement = statement.on_conflict_do_nothing(index_elements=["event_id"]).returning(GPSEvent.event_id)

        try:

            result = self.session.execute(statement)

            inserted_event_id = result.scalar_one_or_none()
            self.session.commit()

            return inserted_event_id is not None

        except Exception:

            self.session.rollback()
            raise



    def find_by_id(self, event_id: str):

        statement = select(GPSEvent).where(GPSEvent.event_id == event_id)

        return self.session.scalar(statement)