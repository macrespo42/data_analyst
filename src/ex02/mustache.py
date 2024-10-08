from typing import Any

import matplotlib.pyplot as plt
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
    cursor.execute("SELECT price FROM customers WHERE event_type='purchase';")
    return cursor.fetchall()


def get_avg_basket() -> list[tuple[Any, ...]]:
    connection = connect_db()

    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT 
            AVG(session_total) AS average_basket_price
        FROM (
            SELECT 
                user_id, 
                SUM(price) AS session_total
            FROM customers
            WHERE event_type = 'purchase'
            GROUP BY user_id, user_session
        ) AS session_totals
        GROUP BY user_id
                """
    )
    return cursor.fetchall()


def describe_prices(prices: list[float]) -> None:
    count = len(prices)
    mean_price = np.mean(prices)
    std_price = np.std(prices)
    min_price = np.min(prices)
    quartiles = np.percentile(prices, [25, 50, 75])
    max_price = np.max(prices)

    print(f"count {count:.6f}")
    print(f"mean {mean_price:.6f}")
    print(f"std {std_price:.6f}")
    print(f"min {min_price:.6f}")
    print(f"25% {quartiles[0]:.6f}")
    print(f"50% {quartiles[1]:.6f}")
    print(f"75% {quartiles[2]:.6f}")
    print(f"max {max_price:.6f}")


def boxplots(prices: list[float], average_basket: list[float]) -> None:
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 6))
    ax1.boxplot(prices, vert=False)

    ax1.set_title("Boxplot")
    ax1.set_yticks([])
    ax1.set_xticks(range(-50, 301, 50))

    boxprops = dict(facecolor="green", edgecolor="black")
    medianprops = dict(linestyle="-", linewidth=2, color="black")
    ax2.boxplot(
        prices,
        vert=False,
        widths=0.5,
        notch=True,
        boxprops=boxprops,
        medianprops=medianprops,
        showfliers=False,
        patch_artist=True,
    )
    ax2.set_yticks([])
    ax2.set_xticks(range(0, 13, 2))
    ax2.set_title("Interquartile range (IQR)")

    ax3.boxplot(
        average_basket,
        vert=False,
        widths=0.5,
        notch=True,
        showfliers=False,
    )
    ax3.set_title("Average basket price")
    ax3.set_yticks([])
    # ax3.set_xticks(range(27, 43, 2))

    plt.tight_layout()
    plt.savefig("boxplot.png")


def main() -> None:
    data = get_items_price()
    prices = [float(price[0]) for price in data]

    data = get_avg_basket()
    avg_basket = [float(basket[0]) for basket in data]

    describe_prices(prices)
    boxplots(prices, avg_basket)


if __name__ == "__main__":
    main()
