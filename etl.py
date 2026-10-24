"""Выгрузка витрин в data/
Запуск:  python etl.py
"""
import duckdb
from pathlib import Path


def count(table):
    return db.sql(f"SELECT count(*) FROM {table}").fetchall()[0][0]


if __name__ == '__main__':
    ROOT = Path(__file__).parent
    db = duckdb.connect(ROOT / "warehouse.duckdb")

    for sql in ["01_clean.sql", "02_mart_daily.sql"]:
        db.execute((ROOT / "sql" / sql).read_text(encoding="utf-8"))

    for t in ["mart_daily", "mart_anomalies"]:
        db.execute(f"COPY {t} TO 'data/{t}.csv' (HEADER, DELIMITER ',')")

    raw = count("read_csv_auto('data/orders_raw.csv')")
    stg = count("stg_orders")

    mart = count("mart_daily")
    anom = count("mart_anomalies")

    print(f"raw {raw} -> stg {stg} (dedup/фильтры) -> mart_daily {mart} дней, аномалий: {anom}")
    print(db.sql("SELECT * FROM mart_anomalies").df().to_string(index=False))
