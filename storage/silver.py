import json
from datetime import datetime, timezone
from pathlib import Path


class SilverStorage:

    def __init__(self, base_path="data/silver"):

        self.base_path = Path(base_path)

    def save(self, event):

        saved_at = datetime.now(timezone.utc)

        directory = (
            self.base_path 
            / f"year{saved_at.year}" 
            / f"month={saved_at.month:02d}" 
            / f"day={saved_at.day:02d}")

        directory.mkdir(parents=True, exist_ok=True)

        filename = directory / f"{event['event_id']}.json"

        with open(filename, "w") as file:
            json.dump(event, file, indent=4)
