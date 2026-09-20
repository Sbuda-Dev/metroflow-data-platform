from warehouse.loader import WarehouseLoader

class FakeRepository:

    def __init__(self):
        self.saved = []

    def save(self, performance):
        self.saved.append(performance)

    def test_warehouse_loader_loads_bus_performance():

        events =  [
        {
            "bus_id": "B101",
            "speed": 40.0
        },
        {
            "bus_id": "B101",
            "speed": 50.0
        },
        {
            "bus_id": "B101",
            "speed": 60.0
        }
    ]

        repository = FakeRepository()

        loader = WarehouseLoader(repository)

        result = loader.load(events)

        assert result ==  [
            {
                "bus_id": "B101",
                "event_count": 3,
                "average_speed": 50.0,
                "minimum_speed": 40.0,
                "maximum_speed": 60.0
            }
        ]

        assert repository.saved == result