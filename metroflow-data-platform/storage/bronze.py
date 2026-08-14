import json
from pathlib import Path
from datetime import datetime

class BronzeStorage:

    def __init__(self):

        self.storage_path = Path("data/bronze")

        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save (self, event):

        today = datetime.utcnow()

        directory = (
            Path("data") 
            / "bronze" 
            / f"year={today.year}" 
            / f"month={today.month:02d}" 
            / f"day={today.day:02d}")

        directory.mkdir(parents=True, exist_ok=True)

        filename = self.storage_path / f"{event['event_id']}.json"

        with open (filename, "w") as file:

            json.dump(event, file, indent=4)