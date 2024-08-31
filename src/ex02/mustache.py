from typing import Any

import numpy as np
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


def get_items_price() -> list[tuple[Any, ...]]:
    connection = connect_db()

    cursor = connection.cursor()
    cursor.execute("SELECT event_type, price FROM customers;")
    return cursor.fetchall()


def describe_prices() -> None:
    data = get_items_price()
    prices = [price for event_type, price in data if event_type == "purchase"]

    count = len(prices)
    # mean_price = np.mean(prices)
    # std_price = np.std(prices)
    # min_price = np.min(prices)
    # quartiles = np.percentile(prices, [25, 50, 75])
    # max_price = np.max(prices)

    print(f"count {count:.6f}")
    # print(f"mean {mean_price:.6f}")
    # print(f"std {std_price:.6f}")
    # print(f"min {min_price:.6f}")
    # print(f"25% {quartiles[0]:.6f}")
    # print(f"50% {quartiles[1]:.6f}")
    # print(f"75% {quartiles[2]:.6f}")
    # print(f"max {max_price:.6f}")


if __name__ == "__main__":
    describe_prices()
