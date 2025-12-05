import duckdb
import pandas as pd
from pathlib import Path
import logging
from validation import get_co2_schema
import pandera as pa

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def transform_data():
    sql_dir = Path("src/sql")
    processed_path = Path("data/processed/co2_data.parquet")
    
    con = duckdb.connect(database=":memory:")
    logging.info("DuckDB connection established.")

    # 1. Clean and Cast
    with open(sql_dir / "01_clean_and_cast.sql", "r") as f:
        con.execute("CREATE OR REPLACE VIEW cleaned_data AS " + f.read())
    
    # 2. Add Metrics (Placeholder)
    with open(sql_dir / "02_calculate_metrics.sql", "r") as f:
        con.execute("CREATE OR REPLACE VIEW metrics_data AS " + f.read())

    # 3. Rolling Averages
    with open(sql_dir / "03_add_rolling_averages.sql", "r") as f:
        con.execute("CREATE OR REPLACE TABLE final_data AS " + f.read())
    
    # Fetch result
    df = con.execute("SELECT * FROM final_data").fetchdf()
    con.close()
    
    # Validate
    logging.info("Validating data schema...")
    try:
        schema = get_co2_schema()
        df = schema.validate(df, lazy=True)
        logging.info("Validation Passed.")
    except Exception as e:
        logging.warning(f"Validation Warning: {e}")

    # Save
    df.to_parquet(processed_path, index=False)
    logging.info(f"Saved processed data to {processed_path}")

if __name__ == "__main__":
    transform_data()