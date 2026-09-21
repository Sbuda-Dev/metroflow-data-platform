import sys

from storage.silver_reader import SilverReader
from database.connection import SessionLocal
from database.repositories import BusPerformanceRepository
from warehouse.job import WarehouseJob
from warehouse.loader import WarehouseLoader
from warehouse.pipeline import WarehousePipeline
from warehouse.config import SILVER_DATA_PATH

def main():

    reader = SilverReader(SILVER_DATA_PATH)

    session = SessionLocal()

    try:
        repository = BusPerformanceRepository(session)

        loader = WarehouseLoader(repository)

        pipeline = WarehousePipeline(loader)

        job = WarehouseJob(reader, pipeline)

        result = job.run()

        print("Warehouse job completed")
        print(f"Events read: {result['events_read']}")
        print(f"Performance records: {len(result['performance'])}")
        print(f"Errors: {len(result['errors'])}")

        if result["errors"]:

            print("Warehouse job failed because some Silver files could not be processed.")

            return 1

        return 0

    finally:

        session.close()

if __name__ == "__main__":
    
    sys.exit(main())