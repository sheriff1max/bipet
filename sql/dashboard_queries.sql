-- SQL для карточек дашборда (в Metabase/Superset вставляются как есть).
-- 1. KPI за период
SELECT sum(revenue) AS revenue, sum(orders) AS orders,
       round(sum(revenue) * 1.0 / sum(orders)) AS aov
FROM mart_daily WHERE order_date BETWEEN :start AND :end;

-- 2. Динамика выручки + бейслайн
SELECT order_date, revenue, revenue_base, revenue_dev_pct
FROM mart_daily
ORDER BY 1;

-- 3. Выручка по городам / каналам / категориям
SELECT city, sum(revenue) AS revenue
FROM mart_orders
GROUP BY 1
ORDER BY 2 DESC;

SELECT channel, date_trunc('week', order_date) AS week, sum(revenue) AS revenue
FROM mart_orders
GROUP BY 1, 2
ORDER BY 2;

SELECT category, sum(revenue) AS revenue, sum(qty) AS units
FROM mart_orders
GROUP BY 1
ORDER BY 2 DESC;

-- 4. Аномалии
SELECT * FROM mart_anomalies;
