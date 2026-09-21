import json

from storage.silver_reader import SilverReader

def test_silver_reader_reads_json_files(tmp_path):

    silver_directory = tmp_path / "silver"

    silver_directory.mkdir()

    event = {
        "event_id": "event-1",
        "received_at": "2026-09-21T10:00:00+00:00",
        "bus_id": "B101",
        "speed": 50.0
    }

    event_file = silver_directory / "event-1.json"

    with open(event_file, "w") as file:
        json.dump(event, file)

    reader = SilverReader(silver_directory)

    events = reader.read_all()

    assert events == [event]

def test_silver_reader_skips_malformed_json(tmp_path):

    silver_directory = tmp_path / "silver"

    silver_directory.mkdir()

    valid_event = {
        "event_id": "event-1",
        "bus_id": "B101",
        "speed": 50.0
    }

    valid_file = silver_directory / "valid.json"

    with open(valid_file, "w") as file:
        json.dump(valid_event, file)

    invalid_file = silver_directory / "invalid.json"

    with open(invalid_file, "w") as file:
        file.write("{ invalid json")

    reader = SilverReader(silver_directory)

    events = reader.read_all()

    assert events == [valid_event]
    assert len(reader.errors) == 1
    assert reader.errors[0]["file"] == str(invalid_file)