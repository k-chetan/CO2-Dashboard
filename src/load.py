import duckdb
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data_to_duckdb():
    PARQUET_PATH = Path("data/processed/co2_data.parquet")
    DB_PATH = Path("data/co2_data.duckdb")
    TABLE_NAME = "co2_emissions"

    if not PARQUET_PATH.exists():
        logging.error(f"Input file missing: {PARQUET_PATH}")
        raise FileNotFoundError("Pipeline sequence error: Transform step must run before Load.")

    logging.info(f"Connecting to persistent database: {DB_PATH}")
    con = duckdb.connect(database=str(DB_PATH), read_only=False)
    
    query = f"CREATE OR REPLACE TABLE {TABLE_NAME} AS SELECT * FROM read_parquet('{str(PARQUET_PATH)}');"
    con.execute(query)
    
    logging.info(f"Table '{TABLE_NAME}' successfully loaded.")
    count = con.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()
    logging.info(f"Verification: {count} records in table.")
    con.close()

if __name__ == "__main__":
    load_data_to_duckdb()
