from pathlib import Path

class ProcessedEventStore:

    def __init__(self, base_path="data/processed"):

        self.base_path = Path(base_path)

    def exists(self, event_id):

        event_file = self.base_path / f"{event_id}.processed"

        return event_file.exists()
    
    def mark_processed(self, event_id):

        self.base_path.mkdir(parents=True, exist_ok=True)

        event_file = self.base_path / f"{event_id}.processed"

        event_file.touch()