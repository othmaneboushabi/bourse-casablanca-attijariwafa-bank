{{ config(materialized='table') }}

WITH price_data AS (
    SELECT
        date_key,
        stock_key,
        close_price
    FROM {{ ref('fact_daily_prices') }}
)

SELECT
    date_key,
    stock_key,
    close_price,
    -- Calcul du rendement quotidien : (Prix du jour - Prix de la veille) / Prix de la veille
    (close_price - LAG(close_price) OVER (PARTITION BY stock_key ORDER BY date_key)) / 
        NULLIF(LAG(close_price) OVER (PARTITION BY stock_key ORDER BY date_key), 0) AS daily_return,
    
    -- Moyennes mobiles sur 20 et 50 jours
    AVG(close_price) OVER (PARTITION BY stock_key ORDER BY date_key ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS moving_average_20,
    AVG(close_price) OVER (PARTITION BY stock_key ORDER BY date_key ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) AS moving_average_50
FROM price_data