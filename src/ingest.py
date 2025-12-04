import requests
from pathlib import Path
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SOURCE_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
RAW_DATA_DIR = Path("data/raw")
RAW_DATA_FILE = RAW_DATA_DIR / "owid-co2-data.csv"

def ingest_data():
    logging.info(f"Starting ingestion from {SOURCE_URL}")
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(SOURCE_URL, timeout=30)
        response.raise_for_status()
        with open(RAW_DATA_FILE, "wb") as f:
            f.write(response.content)
        logging.info(f"Ingestion complete. Data saved to {RAW_DATA_FILE}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ingestion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    ingest_data()
