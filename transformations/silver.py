import json
from pathlib import Path

class SilverTransformer:

    def transform_event(self, bronze_event: dict) -> dict:

        payload = bronze_event["payload"]

        return {
            "event_id": bronze_event["event_id"],
            "received_at": bronze_event["received_at"],
            "event_type": bronze_event["event_type"],
            "source": bronze_event["source"],
            "bus_id": payload["bus_id"],
            "speed": payload["speed"]
        }

    def transform_file(self, bronze_file: Path, silver_file: Path) -> None:

        bronze_event = json.loads(bronze_file.read_text())

        silver_event = self.transform_event(bronze_event)

        silver_file.parent.mkdir(parents=True, exist_ok=True)

        silver_file.write_text(json.dumps(silver_event, indent=2))

