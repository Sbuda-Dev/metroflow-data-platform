import os

from dotenv import load_dotenv

load_dotenv()

SILVER_DATA_PATH = os.getenv("SILVER_DATA_PATH", "data/silver")