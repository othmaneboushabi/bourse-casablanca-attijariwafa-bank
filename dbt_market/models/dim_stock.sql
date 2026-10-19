{{ config(materialized='table') }}

WITH source_data AS (
    SELECT DISTINCT
        ticker,
        company_name
    FROM {{ source('market_data', 'stg_stock_prices') }}
)

SELECT
    -- md5 permet de générer une clé technique unique (stock_key) basée sur le Ticker
    md5(ticker) AS stock_key,
    ticker,
    company_name,
    'Non renseigné' AS sector  -- Le secteur n'était pas dans l'export, on le prépare pour plus tard
FROM source_data