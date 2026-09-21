from storage.silver_reader import SilverReader
from warehouse.pipeline import WarehousePipeline

class WarehouseJob:

    def __init__(self, reader, pipeline):
        self.reader = reader
        self.pipeline = pipeline

    def run(self):

        events = self.reader.read_all()

        performance = self.pipeline.run(events)

        return {
            "events_read": len(events),
            "performance": performance,
            "errors": self.reader.errors
        }

