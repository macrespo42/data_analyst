from typing import Any

import matplotlib.pyplot as plt
import psycopg2


def connect_db():
    host = "db"
    port = "5432"
    dbname = "piscineds"
    user = "macrespo"
    password = "mysecretpassword"

    try:
        connection = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=user, password=password
        )
        return connection

    except Exception as e:
        print("Error when connecting to postgres: ", e)
        exit(1)


def get_customers_orders_frequencies() -> list[tuple[Any, ...]]:
    connection = connect_db()

    cursor = connection.cursor()
    cursor.execute(
        """SELECT count(*)
        FROM customers
        WHERE event_type='purchase'
        GROUP BY user_id
        HAVING count(*) BETWEEN 0 and 40;"""
    )
    return cursor.fetchall()


def get_customers_spends_frequencies() -> list[tuple[Any, ...]]:
    connection = connect_db()

    cursor = connection.cursor()
    cursor.execute(
        """SELECT sum(price)
        FROM customers
        WHERE event_type='purchase'
        GROUP BY user_id
        HAVING sum(price) BETWEEN 0 and 201;"""
    )
    return cursor.fetchall()


def barplot(orders, spends) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.hist(orders, bins=5, width=8, alpha=0.3)
    ax1.grid(True, zorder=-1)
    ax1.set_title("frequency of customers order")
    ax1.set_ylabel("customers")
    ax1.set_xlabel("frequency")
    ax1.set_xticks(range(0, 40, 10))
    ax1.set_yticks(range(0, 60_001, 10_000))

    ax2.hist(spends, bins=5)
    ax2.grid(True, zorder=-1)
    ax2.set_title("frequency of customers spends")
    ax2.set_ylabel("customers")
    ax2.set_xlabel("monetary value in A")
    ax2.set_yticks(range(0, 40_001, 5_000))
    ax2.set_xticks(range(0, 201, 50))
    ax2.set_ylim(40_000)

    plt.savefig("order_frequencies.png")


def main() -> None:
    data = get_customers_orders_frequencies()
    orders = [float(order[0]) for order in data]

    data = get_customers_spends_frequencies()
    spends = [float(spend[0]) for spend in data]

    barplot(orders, spends)


if __name__ == "__main__":
    main()
