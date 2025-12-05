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