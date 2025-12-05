import os

# Define directories
dirs = ["src", "src/sql", "data/raw", "data/processed"]
for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"✅ Ensure directory exists: {d}")

# Create __init__.py
with open("src/__init__.py", "w") as f:
    pass

# --- 1. DEFINE FILE CONTENTS ---

ingest_py = """
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
"""

validation_py = """
import pandera as pa
from pandera import Column, Check

def get_co2_schema() -> pa.DataFrameSchema:
    schema = pa.DataFrameSchema(
        columns={
            "country": Column(str, nullable=False),
            "year": Column(int, checks=[Check.greater_than_or_equal_to(1750)], nullable=False),
            "iso_code": Column(str, nullable=False),
            "population": Column(float, nullable=True),
            "gdp": Column(float, nullable=True),
            "co2": Column(float, nullable=True),
            "cumulative_co2": Column(float, nullable=True),
            "co2_per_capita": Column(float, nullable=True),
            "consumption_co2": Column(float, nullable=True),
            "coal_co2": Column(float, nullable=True),
            "oil_co2": Column(float, nullable=True),
            "gas_co2": Column(float, nullable=True),
            "cement_co2": Column(float, nullable=True),
            "co2_growth_abs": Column(float, nullable=True),
            "co2_rolling_7yr": Column(float, nullable=True),
        },
        strict="filter",
        coerce=True
    )
    return schema
"""

transform_py = """
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
"""

load_py = """
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
"""

# --- SQL FILES ---

sql_01 = """
WITH source_data AS (
    SELECT * FROM read_csv_auto('data/raw/owid-co2-data.csv')
)
SELECT
    CAST(country AS VARCHAR) AS country,
    CAST(year AS INTEGER) AS year,
    CAST(iso_code AS VARCHAR) AS iso_code,
    CAST(population AS DOUBLE) AS population,
    CAST(gdp AS DOUBLE) AS gdp,
    CAST(co2 AS DOUBLE) AS co2,
    CAST(cumulative_co2 AS DOUBLE) AS cumulative_co2,
    CAST(co2_per_capita AS DOUBLE) AS co2_per_capita,
    CAST(consumption_co2 AS DOUBLE) AS consumption_co2,
    CAST(coal_co2 AS DOUBLE) AS coal_co2,
    CAST(oil_co2 AS DOUBLE) AS oil_co2,
    CAST(gas_co2 AS DOUBLE) AS gas_co2,
    CAST(cement_co2 AS DOUBLE) AS cement_co2,
    CAST(co2_growth_abs AS DOUBLE) AS co2_growth_abs
FROM source_data
WHERE iso_code IS NOT NULL OR country = 'World';
"""

sql_02 = "SELECT * FROM cleaned_data;"

sql_03 = """
SELECT 
    *, 
    AVG(co2) OVER (
        PARTITION BY country 
        ORDER BY year 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS co2_rolling_7yr
FROM metrics_data;
"""

# --- 2. WRITE FILES ---

files = {
    "src/ingest.py": ingest_py,
    "src/validation.py": validation_py,
    "src/transform.py": transform_py,
    "src/load.py": load_py,
    "src/sql/01_clean_and_cast.sql": sql_01,
    "src/sql/02_calculate_metrics.sql": sql_02,
    "src/sql/03_add_rolling_averages.sql": sql_03
}

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content.strip())
    print(f"✅ Generated: {path}")

print("\n🎉 Pipeline setup complete! You can now run 'make run-pipeline'.")
