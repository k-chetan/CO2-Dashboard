SELECT
    *,
    CASE WHEN gdp > 0 THEN co2 / gdp ELSE NULL END AS co2_per_gdp,
    CASE WHEN co2 > 0 THEN (coal_co2 / co2) ELSE 0 END AS coal_share,
    CASE WHEN co2 > 0 THEN (oil_co2 / co2) ELSE 0 END AS oil_share,
    CASE WHEN co2 > 0 THEN (gas_co2 / co2) ELSE 0 END AS gas_share
FROM cleaned_data;
