from transformations.gold import calculate_bus_performance

class WarehousePipeline:

    def __init__(self, loader):
        self.loader = loader

    def run(self, events):

        performance = calculate_bus_performance(events)

        self.loader.load(performance)

        return performance

