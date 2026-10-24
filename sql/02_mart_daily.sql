-- Дневная витрина метрик + контроль отклонений.
-- Бейслайн: медиана того же дня недели за 4 предыдущие недели.
-- Так недельная сезонность не попадает в "аномалии", а медиана устойчива к выбросам.
CREATE OR REPLACE TABLE mart_daily AS
WITH d AS (
    SELECT
        order_date,
        sum(revenue)                          AS revenue,
        count(*)                              AS orders,
        sum(qty)                              AS units,
        round(sum(revenue) * 1.0 / count(*))  AS aov
    FROM mart_orders
    GROUP BY 1
),
w AS (
    SELECT
        *,
        dayofweek(order_date) AS dow
    FROM d
),
b AS (
    SELECT
        *,
        median(revenue) OVER (
            PARTITION BY dow
            ORDER BY order_date
            ROWS BETWEEN 4 PRECEDING AND 1 PRECEDING
        ) AS revenue_base
    FROM w
)
SELECT
    order_date, revenue, orders, units, aov,
    round(revenue_base) AS revenue_base,
    round(100.0 * (revenue - revenue_base) / nullif(revenue_base, 0), 1) AS revenue_dev_pct
FROM b;

-- Флаги аномалий: |отклонение| > 60% к бейслайну того же дня недели
CREATE OR REPLACE TABLE mart_anomalies AS
SELECT order_date, revenue, revenue_base, revenue_dev_pct
FROM mart_daily
WHERE abs(revenue_dev_pct) > 60
ORDER BY order_date;
