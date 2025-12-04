import pandera as pa
from pandera import Column, Check

def get_co2_schema() -> pa.DataFrameSchema:
    schema = pa.DataFrameSchema(
        columns={
            "country": Column(str, nullable=False),
            "year": Column(int, checks=[Check.greater_than_or_equal_to(1750)], nullable=False),
            "iso_code": Column(str, nullable=False),
            "population": Column(float, checks=[Check.greater_than_or_equal_to(0)], nullable=True, coerce=True),
            "gdp": Column(float, checks=[Check.greater_than_or_equal_to(0)], nullable=True),
            "co2": Column(float, checks=[Check.greater_than_or_equal_to(0)], nullable=True),
            "cumulative_co2": Column(float, checks=[Check.greater_than_or_equal_to(0)], nullable=True),
            "coal_co2": Column(float, checks=[Check.greater_than_or_equal_to(0)], nullable=True),
            "oil_co2": Column(float, checks=[Check.greater_than_or_equal_to(0)], nullable=True),
            "gas_co2": Column(float, checks=[Check.greater_than_or_equal_to(0)], nullable=True),
            "cement_co2": Column(float, checks=[Check.greater_than_or_equal_to(0)], nullable=True),
            "flaring_co2": Column(float, checks=[Check.greater_than_or_equal_to(0)], nullable=True),
            "co2_rolling_7yr_avg": Column(float, nullable=True),
            "co2_per_gdp": Column(float, nullable=True),
            "coal_share": Column(float, checks=[Check.in_range(0, 1)], nullable=True),
        },
        strict="filter",
        ordered=False
    )
    return schema
