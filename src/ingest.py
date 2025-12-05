import requests
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ingest_data():
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    output_path = Path("data/raw/owid-co2-data.csv")
    
    logging.info(f"Downloading raw data from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        logging.info(f"Successfully saved data to {output_path}")
        
    except Exception as e:
        logging.error(f"Failed to ingest data: {e}")
        raise

if __name__ == "__main__":
    ingest_data()