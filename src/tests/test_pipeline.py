import pytest
import pandas as pd
import duckdb
import pandera as pa
from pathlib import Path
from src.validation import get_co2_schema

# ==============================================================================
# 1. TEST SQL LOGIC (The Rolling Average)
# ==============================================================================
def test_rolling_average_calculation():
    """
    Verifies that the SQL script '03_add_rolling_averages.sql' correctly 
    calculates a 7-year rolling average using a known dataset.
    """
    # 1. Setup Mock Data (Simple sequence: 1, 2, 3...)
    # We expect the 7th value (year 2006) to be avg(1,2,3,4,5,6,7) = 4.0
    mock_df = pd.DataFrame({
        'country': ['Testland'] * 10,
        'year': range(2000, 2010),
        'co2': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        # Add dummy columns required by select *
        'iso_code': ['TST'] * 10,
        'population': [100.0] * 10,
        'gdp': [1000.0] * 10,
        'cumulative_co2': [0.0] * 10,
        'co2_per_capita': [0.0] * 10,
        'share_global_co2': [0.0] * 10,
        'co2_growth_abs': [0.0] * 10,
        'consumption_co2': [0.0] * 10,
        'coal_co2': [0.0] * 10,
        'oil_co2': [0.0] * 10,
        'gas_co2': [0.0] * 10,
        'cement_co2': [0.0] * 10,
        'flaring_co2': [0.0] * 10
    })

    # 2. Initialize Ephemeral DuckDB
    con = duckdb.connect(database=":memory:")
    con.register('metrics_data', mock_df) # Register DF as SQL table

    # 3. Read & Execute the actual SQL Logic file
    sql_path = Path("src/sql/03_add_rolling_averages.sql")
    if not sql_path.exists():
        pytest.fail(f"SQL file not found at {sql_path}")
        
    with open(sql_path, "r") as f:
        query = "CREATE OR REPLACE TABLE result AS " + f.read()
        con.execute(query)

    # 4. Fetch Result
    result_df = con.execute("SELECT year, co2, co2_rolling_7yr FROM result ORDER BY year").fetchdf()
    
    # 5. Assert Math
    # Year 2000 (1st year): Rolling avg should be 1.0 (only 1 value)
    assert result_df.iloc[0]['co2_rolling_7yr'] == 1.0
    
    # Year 2006 (7th year): Avg of 1..7 should be 4.0
    # (1+2+3+4+5+6+7) / 7 = 28 / 7 = 4.0
    val_2006 = result_df[result_df['year'] == 2006]['co2_rolling_7yr'].values[0]
    assert val_2006 == 4.0, f"Expected 4.0, got {val_2006}"

    con.close()

# ==============================================================================
# 2. TEST SCHEMA VALIDATION (The Guardrails)
# ==============================================================================
def test_schema_rejects_bad_data():
    """
    Verifies that Pandera correctly raises a SchemaError when fed invalid data.
    """
    schema = get_co2_schema()

    # Case 1: Negative Year (Should fail)
    bad_df_year = pd.DataFrame({
        'country': ['BadLand'],
        'year': [1700], # Schema requires >= 1750
        'iso_code': ['BAD']
    })
    
    with pytest.raises(pa.errors.SchemaError):
        schema.validate(bad_df_year)

    # Case 2: Null ISO Code (Should fail)
    bad_df_iso = pd.DataFrame({
        'country': ['BadLand'],
        'year': [2020], 
        'iso_code': [None] # Schema requires non-nullable
    })

    with pytest.raises(pa.errors.SchemaError):
        schema.validate(bad_df_iso)

# ==============================================================================
# 3. TEST FILE STRUCTURE
# ==============================================================================
def test_directory_structure():
    """
    Ensures the rigorous directory structure is maintained.
    """
    required_dirs = [
        Path("data/raw"),
        Path("data/processed"),
        Path("src/sql"),
        Path("stories")
    ]
    for d in required_dirs:
        assert d.exists(), f"Directory missing: {d}"
