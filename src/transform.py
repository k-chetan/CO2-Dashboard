import duckdb
import pandas as pd
from pathlib import Path
import logging
import pandera as pa
# Corrected import for script execution context
from validation import get_co2_schema

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "co2_data.parquet"
SQL_DIR = Path("src/sql")

def transform_data():
    logging.info("Initializing transformation pipeline...")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(database=":memory:", read_only=False)
    logging.info("DuckDB in-memory connection established.")

    with open(SQL_DIR / "01_clean_and_cast.sql", "r") as f:
        con.execute("CREATE OR REPLACE VIEW cleaned_data AS " + f.read())
    
    with open(SQL_DIR / "02_calculate_metrics.sql", "r") as f:
        con.execute("CREATE OR REPLACE VIEW metrics_data AS " + f.read())
        
    with open(SQL_DIR / "03_add_rolling_averages.sql", "r") as f:
        con.execute("CREATE OR REPLACE TABLE final_data AS " + f.read())

    final_df = con.execute("SELECT * FROM final_data").fetchdf()
    logging.info(f"Transformation complete. Result shape: {final_df.shape}")

    logging.info("Validating data against schema...")
    schema = get_co2_schema()
    try:
        schema.validate(final_df, lazy=True)
        logging.info("Validation passed successfully.")
    except pa.errors.SchemaErrors as err:
        logging.error("Validation FAILED. Schema errors detected:")
        logging.error(err.failure_cases)
        raise

    final_df.to_parquet(OUTPUT_FILE, index=False)
    logging.info(f"Data successfully serialized to {OUTPUT_FILE}")
    con.close()

if __name__ == "__main__":
    transform_data()
