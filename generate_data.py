"""Генерит сырые заказы интернет-магазина: data/orders_raw.csv
Сознательно добавляет дубли, пропуски, отмены закаков, promo-всплеск.
"""
import random
from datetime import date, timedelta


if __name__ == '__main__':
    random.seed(42)

    CITIES = ["Москва", "СПб", "Казань", "Екатеринбург"]
    CHANNELS = ["organic", "paid", "email"]
    CATS = {"Электроника": 12000, "Одежда": 3500, "Дом": 5000}

    start, days = date(2025, 1, 1), 180
    rows, oid = [], 1

    # осознанная аномалия: promo x2.2
    PROMO = [(date(2025, 3, 10), date(2025, 3, 14))]

    for d in (start + timedelta(days=i) for i in range(days)):
        weekend = 1.35 if d.weekday() >= 5 else 0.85
        n = round(random.gauss(24 * weekend, 2))
        if any(a <= d <= b for a, b in PROMO):
            n = round(n * 2.2)
        for _ in range(n):
            cat = random.choice(list(CATS))
            price = int(CATS[cat] * random.uniform(0.75, 1.3))
            rows.append([
                f"O{oid}",
                d.isoformat(),
                random.choice(CITIES),
                random.choice(CHANNELS),
                cat,
                price,
                random.randint(1, 3),
                "cancelled" if random.random() < 0.12 else "paid"
            ])
            # дубль
            if random.random() < 0.03:
                rows.append(rows[-1][:])
            # пропуск
            if random.random() < 0.02:
                rows[-1][2] = None
            oid += 1

    with open("data/orders_raw.csv", "w", encoding="utf-8") as f:
        f.write("order_id,order_date,city,channel,category,price,qty,status\n")
        f.write("\n".join(",".join("" if v is None else str(v) for v in r) for r in rows))

    print(f"rows: {len(rows)}")
