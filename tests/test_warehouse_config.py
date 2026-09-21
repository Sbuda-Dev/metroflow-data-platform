from warehouse.config import SILVER_DATA_PATH

def test_silver_data_path_has_default_value():

    assert SILVER_DATA_PATH == "data/silver"