from transformations.gps import transform_gps_event
from transformations.validators import validate_gps_event
from storage.silver import SilverStorage
from storage.quarantine import QuarantineStorage
from storage.processed import ProcessedEventStore


class EventPipeline:

    def __init__(self, silver_storage=None, quarantine_storage=None, processed_store=None):

        self.silver_storage = (silver_storage or SilverStorage())
        self.quarantine_storage = (quarantine_storage or QuarantineStorage())
        self.processed_store = (processed_store or ProcessedEventStore())

    def process(self, event):

        event_id = event["event_id"]

        if self.processed_store.exists(event_id):

            return {
                "status": "duplicate",
                "event_id": event_id
            }

        try:

            validate_gps_event(event)

            silver_event = transform_gps_event(event)

            self.silver_storage.save(silver_event)

            self.processed_store.mark_processed(event_id)

            return {
                "status": "processed",
                "event": silver_event
            }

        except ValueError as error:

            self.quarantine_storage.save(event, str(error))

            return {
                "status": "quarantined",
                "reason": str(error)
            }