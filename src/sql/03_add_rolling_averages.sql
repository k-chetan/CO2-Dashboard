SELECT 
    *, 
    AVG(co2) OVER (
        PARTITION BY country 
        ORDER BY year 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS co2_rolling_7yr
FROM metrics_data;