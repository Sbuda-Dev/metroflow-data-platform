from warehouse.validators import validate_bus_performance


class WarehouseLoader:

    def __init__(self, repository):
        self.repository = repository

    def load(self, performance):

        for bus_performance in performance:

            validate_bus_performance(bus_performance)

            self.repository.save(bus_performance)

        return performance