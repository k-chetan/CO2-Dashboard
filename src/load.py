import duckdb
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data():
    input_path = Path("data/processed/co2_data.parquet")
    db_path = Path("data/co2_data.duckdb")
    
    if not input_path.exists():
        raise FileNotFoundError("Processed data not found. Run transform.py first.")

    con = duckdb.connect(str(db_path))
    con.execute(f"CREATE OR REPLACE TABLE co2_emissions AS SELECT * FROM read_parquet('{input_path}')")
    con.close()
    logging.info(f"Loaded data into DuckDB at {db_path}")

if __name__ == "__main__":
    load_data()