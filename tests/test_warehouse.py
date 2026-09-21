import pytest

from warehouse.pipeline import WarehousePipeline
from database.connection import SessionLocal
from database.repositories import BusPerformanceRepository
from warehouse.loader import WarehouseLoader
from warehouse.silver_pipeline import SilverWarehousePipeline

class FakeLoader:

    def __init__(self):
        self.loaded = []

    def load(self, performance):
        self.loaded = performance
        return performance

class FakeRepository:

    def __init__(self):
        self.saved = []

    def save(self, performance):
        self.saved.append(performance)

class FakeWarehousePipeline:

    def __init__(self):
        self.received_events = None

    def run(self, events):
        self.received_events = events

        return [
            {
                "bus_id": "B500",
                "event_count": 3,
                "average_speed": 50.0,
                "minimum_speed": 30.0,
                "maximum_speed": 70.0
            }
        ]

def test_warehouse_pipeline_calculate_and_loads_performance():

    events = [
        {
            "bus_id": "B101",
            "speed": 40.0
        },
        {
            "bus_id": "B101",
            "speed": 50.0
        },
        {
            "bus_id": "B101",
            "speed": 60.0
        }
    ]

    loader = FakeLoader()

    pipeline = WarehousePipeline(loader)

    result = pipeline.run(events)

    assert result == [
        {
            "bus_id": "B101",
            "event_count": 3,
            "average_speed": 50.0,
            "minimum_speed": 40.0,
            "maximum_speed": 60.0
        }
    ]

    assert loader.loaded == result

def test_warehouse_pipeline_loads_into_postgresql():

    events = [
        {
            "bus_id": "B777",
            "speed": 40.0
        },
        {
            "bus_id": "B777",
            "speed": 50.0
        },
        {
            "bus_id": "B777",
            "speed": 60.0
        }
    ]

    session = SessionLocal()

    try:

        repository = BusPerformanceRepository(session)

        loader = WarehouseLoader(repository)

        pipeline = WarehousePipeline(loader)

        result = pipeline.run(events)

        stored = repository.find_by_bus_id("B777")

        assert result == [
            {
                "bus_id": "B777",
                "event_count": 3,
                "average_speed": 50.0,
                "minimum_speed": 40.0,
                "maximum_speed": 60.0
            }
        ]

        assert stored is not None
        assert stored.bus_id == "B777"
        assert stored.event_count == 3
        assert float(stored.average_speed) == 50.0
        assert float(stored.minimum_speed) == 40.0
        assert float(stored.maximum_speed) == 60.0

    finally:

        session.close()


def test_warehouse_pipeline_updates_existing_bus_performance():

    first_events = [
        {
            "bus_id": "B888",
            "speed": 40.0
        },
        {
            "bus_id": "B888",
            "speed": 50.0
        }
    ]

    second_events = [
        {
            "bus_id": "B888",
            "speed": 60.0
        },
        {
            "bus_id": "B888",
            "speed": 80.0
        },
        {
            "bus_id": "B888",
            "speed": 100.0
        }
    ]

    session = SessionLocal()

    try:

        repository = BusPerformanceRepository(session)
        loader = WarehouseLoader(repository)
        pipeline = WarehousePipeline(loader)

        pipeline.run(first_events)
        pipeline.run(second_events)

        stored = repository.find_by_bus_id("B888")

        assert stored is not None
        assert stored.event_count == 3
        assert float(stored.average_speed) == 80.0
        assert float(stored.minimum_speed) == 60.0
        assert float(stored.maximum_speed) == 100.0

    finally:

        session.close()


def test_silver_events_can_flow_into_warehouse():

    silver_events = [
        {
            "event_id": "event-1",
            "received_at": "2026-09-20T10:00:00+00:00",
            "bus_id": "B500",
            "speed": 30.0
        },
        {
            "event_id": "event-2",
            "received_at": "2026-09-20T10:01:00+00:00",
            "bus_id": "B500",
            "speed": 50.0
        },
        {
            "event_id": "event-3",
            "received_at": "2026-09-20T10:02:00+00:00",
            "bus_id": "B500",
            "speed": 70.0
        }
    ]


    warehouse_pipeline = FakeWarehousePipeline()

    pipeline = SilverWarehousePipeline(warehouse_pipeline)

    result = pipeline.run(silver_events)

    assert result == [
        {
            "bus_id": "B500",
            "event_count": 3,
            "average_speed": 50.0,
            "minimum_speed": 30.0,
            "maximum_speed": 70.0
        }
    ]

    assert warehouse_pipeline.received_events == silver_events

def test_warehouse_loader_rejects_invalid_performance():

    performance = [
        {
            "bus_id": "B101",
            "event_count": 0,
            "average_speed": 50.0,
            "minimum_speed": 40.0,
            "maximum_speed": 60.0
        }
    ]

    repository = FakeRepository()
    loader = WarehouseLoader(repository)

    with pytest.raises(ValueError, match="event_count must be greater than zero"):
        loader.load(performance)

    assert repository.saved == []


def test_multiple_buses_are_loaded_into_warehouse():

    events = [
        {
            "bus_id": "B101",
            "speed": 40.0
        },
        {
            "bus_id": "B101",
            "speed": 50.0
        },
        {
            "bus_id": "B101",
            "speed": 60.0
        },
        {
            "bus_id": "B202",
            "speed": 30.0
        },
        {
            "bus_id": "B202",
            "speed": 50.0
        }
    ]

    session = SessionLocal()

    try:

        repository = BusPerformanceRepository(session)

        loader = WarehouseLoader(repository)

        pipeline = WarehousePipeline(loader)

        result = pipeline.run(events)

        assert len(result) == 2

        b101 = repository.find_by_bus_id("B101")
        b202 = repository.find_by_bus_id("B202")

        assert b101 is not None
        assert b202 is not None

        assert b101.event_count == 3
        assert float(b101.average_speed) == 50.0
        assert float(b101.minimum_speed) == 40.0
        assert float(b101.maximum_speed) == 60.0

        assert b202.event_count == 2
        assert float(b202.average_speed) == 40.0
        assert float(b202.minimum_speed) == 30.0
        assert float(b202.maximum_speed) == 50.0

    finally:

        session.close()