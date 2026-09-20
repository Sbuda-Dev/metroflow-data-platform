from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import GPSEvent, BusPerformance
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


class BusPerformanceRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, performance: dict):

        existing = self.find_by_bus_id(performance["bus_id"])

        try:

            event_count = int(performance["event_count"])
            average_speed = float(performance["average_speed"])
            minimum_speed = float(performance["minimum_speed"])
            maximum_speed = float(performance["maximum_speed"])

            if existing is None:

                warehouse_record = BusPerformance(
                    bus_id=performance["bus_id"],
                    event_count=event_count,
                    average_speed=average_speed,
                    minimum_speed=minimum_speed,
                    maximum_speed=maximum_speed
                )

                self.session.add(warehouse_record)

            else:

            
                existing.event_count = performance["event_count"]
                existing.average_speed = performance["average_speed"]
                existing.minimum_speed = performance["minimum_speed"]
                existing.maximum_speed = performance["maximum_speed"]
        

            self.session.commit()

        except Exception:

            self.session.rollback()
            raise

    def find_by_bus_id(self, bus_id: str):

        statement = select(BusPerformance).where(BusPerformance.bus_id == bus_id)

        return self.session.scalar(statement)
