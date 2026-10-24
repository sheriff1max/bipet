"""Превью дашборда.
Запуск:  python dashboard.py  ->  dashboard/preview.png
"""
import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

db = duckdb.connect("warehouse.duckdb", read_only=True)
daily = db.sql("SELECT * FROM mart_daily ORDER BY order_date").df()
city = db.sql("SELECT city, sum(revenue) r FROM mart_orders GROUP BY 1 ORDER BY 2 DESC").df()
cat = db.sql("SELECT category, sum(revenue) r FROM mart_orders GROUP BY 1 ORDER BY 2 DESC").df()
anom = db.sql("SELECT * FROM mart_anomalies").df()

fig, ax = plt.subplots(2, 2, figsize=(14, 8))
fig.suptitle("Продажи — дневной мониторинг", fontsize=14)

a = ax[0, 0]
a.plot(daily.order_date, daily.revenue, lw=1, color="#2b6cb0", label="revenue")
a.plot(daily.order_date, daily.revenue_base, lw=1.5, ls="--", color="#a0aec0", label="baseline (тот же ДН, 4 нед)")
a.scatter(anom.order_date, anom.revenue, s=45, color="#e53e3e", zorder=3, label="аномалия")
a.legend(fontsize=8)
a.set_title("Выручка и отклонения")

ax[0, 1].barh(city.city, city.r, color="#2b6cb0")
ax[0, 1].set_title("Выручка по городам")
ax[1, 0].bar(cat.category, cat.r, color="#38a169")
ax[1, 0].set_title("Выручка по категориям")
ax[1, 1].plot(daily.order_date, daily.aov, lw=1, color="#805ad5")
ax[1, 1].set_title("AOV")

for x in ax.flat:
    x.tick_params(labelsize=8)
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig("dashboard/preview.png", dpi=110)
print("dashboard/preview.png")
