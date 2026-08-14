from transformations.gps import transform_gps_event
from transformations.validators import validate_gps_event
from storage.silver import SilverStorage
from storage.quarantine import QuarantineStorage


class EventPipeline:

    def __init__(self, silver_storage=None, quarantine_storage=None):

        self.silver_storage = (silver_storage or SilverStorage())
        self.quarantine_storage = (quarantine_storage or QuarantineStorage())

    def process(self, event):

        try:

            validate_gps_event(event)

            silver_event = transform_gps_event(event)

            self.silver_storage.save(silver_event)

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