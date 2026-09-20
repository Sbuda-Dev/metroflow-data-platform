from transformations.gold import calculate_bus_performance
from database.repositories import BusPerformanceRepository

class WarehouseLoader:

    def __init__(self, repository):
        self.repository = repository

    def load(self, performance):

        for bus_performance in performance:
            self.repository.save(bus_performance)

        return performance