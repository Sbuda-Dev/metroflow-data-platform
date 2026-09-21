import json
from pathlib import Path

class SilverReader:

    def __init__(self, base_path="data/silver"):
        self.base_path = Path(base_path)
        self.errors = []

    def read_all(self):

        events = []

        self.errors = []

        for file_path in self.base_path.rglob("*.json"):

            try:

                with open(file_path, "r") as file:
                    event = json.load(file)

                events.append(event)

            except (json.JSONDecodeError, OSError) as error:

                self.errors.append({"file": str(file_path), "error": str(error)})

        return events


