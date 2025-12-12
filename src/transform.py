import duckdb
import pandas as pd
from pathlib import Path
import logging
import pandera.pandas as pa
from validation import get_co2_schema

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def transform_data():
    sql_dir = Path("src/sql")
    processed_path = Path("data/processed/co2_data.parquet")
    raw_path = Path("data/raw/owid-co2-data.csv") # Local dependency
    
    con = duckdb.connect(database=":memory:")
    logging.info("DuckDB engine started.")

    # --- DE PRINCIPLE: DEPENDENCY INJECTION ---
    # We "inject" the local CSV file as the view 'source_data'.
    # The SQL script doesn't know it's a file; it just sees a table.
    con.execute(f"CREATE OR REPLACE VIEW source_data AS SELECT * FROM read_csv_auto('{raw_path}')")

    # 1. Execute Pure SQL Transformations
    with open(sql_dir / "01_clean_and_cast.sql", "r") as f:
        con.execute("CREATE OR REPLACE VIEW cleaned_data AS " + f.read())
    
    with open(sql_dir / "02_calculate_metrics.sql", "r") as f:
        con.execute("CREATE OR REPLACE VIEW metrics_data AS " + f.read())

    with open(sql_dir / "03_add_rolling_averages.sql", "r") as f:
        con.execute("CREATE OR REPLACE TABLE final_data AS " + f.read())
    
    # 2. Extract & Validate
    df = con.execute("SELECT * FROM final_data").fetchdf()
    con.close()
    
    logging.info("Validating data schema...")
    try:
        schema = get_co2_schema()
        df = schema.validate(df, lazy=True)
        logging.info("✅ Validation Passed.")
    except Exception as e:
        logging.warning(f"Validation Warning: {e}")

    # 3. Save
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(processed_path, index=False)
    logging.info(f"Saved processed data to {processed_path}")

if __name__ == "__main__":
    transform_data()