from warehouse.pipeline import WarehousePipeline

class SilverWarehousePipeline:

    def __init__(self, warehouse_pipeline):
        self.warehouse_pipeline = warehouse_pipeline

    def run(self, silver_events):

        return self.warehouse_pipeline.run(silver_events)