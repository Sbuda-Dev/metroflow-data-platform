from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PostgresSQLUUID

class Base(DeclarativeBase):
    pass

class GPSEvent(Base):

    __tablename__ = "gps_events"

    event_id: Mapped[UUID] = mapped_column(PostgresSQLUUID(as_uuid=True), primary_key=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    bus_id: Mapped[str] = mapped_column(String(50), nullable=False)
    speed: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False)










