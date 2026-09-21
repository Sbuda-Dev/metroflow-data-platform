import json

from warehouse.job import WarehouseJob
from database.connection import SessionLocal
from database.repositories import BusPerformanceRepository
from warehouse.loader import WarehouseLoader
from warehouse.pipeline import WarehousePipeline
from storage.silver_reader import SilverReader

class FakeReader:

    def __init__(self, events=None):

        if events is None:
            events = [
                {
                    "event_id": "event-1",
                    "bus_id": "B101",
                    "speed": 40.0
                },
                {
                    "event_id": "event-2",
                    "bus_id": "B101",
                    "speed": 60.0
                }
            ]

        self.events = events
        self.errors = []

    def read_all(self):
      return self.events


class FakePipeline:

    def __init__(self):
        self.received_events = None

    def run(self, events):
        self.received_events = events

        if not events:
            return []

        return [
            {
                "bus_id": "B101",
                "event_count": 2,
                "average_speed": 50.0,
                "minimum_speed": 40.0,
                "maximum_speed": 60.0
            }
        ]


def test_warehouse_job_reads_silver_and_runs_pipeline():

    reader = FakeReader()
    pipeline = FakePipeline()

    job = WarehouseJob(reader, pipeline)

    result = job.run()

    assert pipeline.received_events ==  [
        {
            "event_id": "event-1",
            "bus_id": "B101",
            "speed": 40.0
        },
        {
            "event_id": "event-2",
            "bus_id": "B101",
            "speed": 60.0
        }
    ]

    assert result ==  {
        "events_read": 2,
        "performance": [
            {
                "bus_id": "B101",
                "event_count": 2,
                "average_speed": 50.0,
                "minimum_speed": 40.0,
                "maximum_speed": 60.0
            }
        ],
        "errors": []
    }

def test_warehouse_job_handles_empty_silver_dataset():

    reader = FakeReader([])
    pipeline = FakePipeline()

    job = WarehouseJob(reader, pipeline)

    result = job.run()

    assert result == {
        "events_read": 0,
        "performance": [],
        "errors": []
    }

    assert pipeline.received_events == []


def test_real_silver_files_flow_into_postgresql(tmp_path):

    silver_path = tmp_path / "silver"

    silver_path.mkdir()

    events = [
        {
            "event_id": "event-101",
            "received_at": "2026-09-21T10:00:00+00:00",
            "bus_id": "B101",
            "speed": 40.0
        },
        {
            "event_id": "event-102",
            "received_at": "2026-09-21T10:01:00+00:00",
            "bus_id": "B101",
            "speed": 60.0
        },
        {
            "event_id": "event-201",
            "received_at": "2026-09-21T10:02:00+00:00",
            "bus_id": "B202",
            "speed": 30.0
        },
        {
            "event_id": "event-202",
            "received_at": "2026-09-21T10:03:00+00:00",
            "bus_id": "B202",
            "speed": 50.0
        }
    ]

    for event in events:

        file_path = silver_path / f"{event['event_id']}.json"

        with open(file_path, "w") as file:
            json.dump(event, file)

    reader = SilverReader(silver_path)

    session = SessionLocal()

    try:
        repository = BusPerformanceRepository(session)

        loader = WarehouseLoader(repository)

        pipeline = WarehousePipeline(loader)

        job = WarehouseJob(reader, pipeline)

        result = job.run()

        assert result["events_read"] == 4
        assert result["errors"] == []

        assert len(result["performance"]) == 2

        b101 = repository.find_by_bus_id("B101")
        b202 = repository.find_by_bus_id("B202")

        assert b101 is not None
        assert b202 is not None

        assert b101.event_count == 2
        assert float(b101.average_speed) == 50.0
        assert float(b101.minimum_speed) == 40.0
        assert float(b101.maximum_speed) == 60.0

        assert b202.event_count == 2
        assert float(b202.average_speed) == 40.0
        assert float(b202.minimum_speed) == 30.0
        assert float(b202.maximum_speed) == 50.0

    finally:

        session.close()


def test_warehouse_job_reports_reader_errors():

    reader = FakeReader([])

    reader.errors = [
        {
            "file": "broken.json",
            "error": "Invalid JSON"
        }]

    pipeline = FakePipeline()

    job = WarehouseJob(reader, pipeline)

    result = job.run()

    assert result["events_read"] == 0

    assert result["errors"] ==  [
        {
            "file": "broken.json",
            "error": "Invalid JSON"
        }
    ]

