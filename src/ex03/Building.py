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
        """WITH purchase_counts AS (
            SELECT user_id, COUNT(*) AS purchase_count
            FROM customers
            WHERE event_type = 'purchase'
            GROUP BY user_id
        )
        SELECT
            CASE
                WHEN purchase_count < 10 THEN 0
                WHEN purchase_count >= 10 AND purchase_count < 20 THEN 10
                WHEN purchase_count >= 20 AND purchase_count < 30 THEN 20
                WHEN purchase_count >= 30 AND purchase_count < 40 THEN 30
                ELSE 40
            END AS purchase_group,
            COUNT(*) AS users_count
        FROM purchase_counts
        GROUP BY purchase_group
        ORDER BY purchase_group;"""
    )
    return cursor.fetchall()


def get_customers_spends_frequencies() -> list[tuple[Any, ...]]:
    connection = connect_db()

    cursor = connection.cursor()
    cursor.execute(
        """WITH purchase_counts AS (
            SELECT user_id, sum(price) AS purchase_count
            FROM customers
            WHERE event_type = 'purchase'
            GROUP BY user_id
        )
        SELECT
            CASE
                WHEN purchase_count < 50 THEN 0
                WHEN purchase_count >= 50 AND purchase_count < 100 THEN 50
                WHEN purchase_count >= 100 AND purchase_count < 150 THEN 100
                WHEN purchase_count >= 150 AND purchase_count < 200 THEN 150
                ELSE 200
            END AS purchase_group,
            COUNT(*) AS users_count
        FROM purchase_counts
        GROUP BY purchase_group
        ORDER BY purchase_group;"""
    )
    return cursor.fetchall()


def barplot(orders_groups, orders, spends_groups, spends) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.bar(orders_groups, orders, width=8)
    ax1.set_title("frequency of customers order")
    ax1.set_ylabel("customers")
    ax1.set_xlabel("frequency")
    ax1.set_xticks(range(0, 40, 10))

    ax2.bar(spends_groups, spends, width=45)
    ax2.set_title("frequency of customers spends")
    ax2.set_ylabel("customers")
    ax2.set_xlabel("monetary value in A")
    ax2.set_xticks(range(0, 201, 50))

    plt.savefig("order_frequencies.png")


def main() -> None:
    data = get_customers_orders_frequencies()
    X = [float(order[0]) for order in data]
    y = [float(order[1]) for order in data]

    data = get_customers_spends_frequencies()
    X1 = [float(order[0]) for order in data]
    y1 = [float(order[1]) for order in data]

    barplot(X, y, X1, y1)


if __name__ == "__main__":
    main()
