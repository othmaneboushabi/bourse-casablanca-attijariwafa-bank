{{ config(materialized='table') }}

SELECT
    date_seance AS date_key,
    md5(ticker) AS stock_key,
    open_price,
    high_price,
    low_price,
    close_price,
    volume_mad,
    volume_titres,
    transactions,
    capitalisation
FROM {{ source('market_data', 'stg_stock_prices') }}