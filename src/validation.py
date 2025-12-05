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