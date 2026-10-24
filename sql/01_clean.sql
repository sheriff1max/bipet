-- Слой очистки: dedup, фильтры, типы. Ничего не агрегируем.
CREATE OR REPLACE TABLE stg_orders AS
SELECT DISTINCT
    order_id,
    TRY_CAST(order_date AS DATE)  AS order_date,
    COALESCE(city, 'Неизвестно')  AS city,
    lower(channel)                AS channel,
    category,
    TRY_CAST(price AS INTEGER)    AS price,
    TRY_CAST(qty AS INTEGER)      AS qty,
    lower(status)                 AS status
FROM read_csv_auto('data/orders_raw.csv', header = true)
WHERE order_date IS NOT NULL
  AND price > 0 AND qty > 0;

-- витрина фактов: только оплаченные заказы
CREATE OR REPLACE TABLE mart_orders AS
SELECT
    order_id,
    order_date,
    city,
    channel,
    category,
    price * qty AS revenue,
    qty
FROM stg_orders
WHERE status = 'paid';
