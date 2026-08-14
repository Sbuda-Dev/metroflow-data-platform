import json
from datetime import datetime, timezone
from pathlib import Path

class QuarantineStorage:

    def __init__(self, base_path="data/quarantine"):
        self.base_path = Path(base_path)

    def save(self, event, reason):

        quarantined_at = datetime.now(timezone.utc)

        directory = (
            self.base_path 
            / f"year={quarantined_at.year}" 
            / f"month={quarantined_at.month:02d}" 
            / f"day={quarantined_at.day:02d}"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        record = {
            "event_id": event["event_id"],
            "quarantined_at": quarantined_at.isoformat(),
            "reason": reason,
            "event": event
        }

        filename = directory / f"{event['event_id']}.json"

        with open(filename, "w") as file:
            json.dump(record, file, indent=4)
    