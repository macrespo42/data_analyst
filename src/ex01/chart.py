import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
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


def get_purchases():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(
        """SELECT date_trunc('day', event_time) AS event_month,
            count(user_id) AS customers_count
        FROM customers 
        WHERE event_type='purchase' 
        AND date_trunc('day', event_time) BETWEEN '2022-10-01'::TIMESTAMP AND '2023-02-28'::TIMESTAMP 
        GROUP BY event_month;"""
    )
    purchases = cursor.fetchall()

    cursor.close()
    connection.close

    return purchases


def get_purchase_prices():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        """SELECT date_trunc('month', event_time) AS event_month, sum(price) as total_price
        FROM customers 
        WHERE event_type='purchase' 
        AND date_trunc('month', event_time) BETWEEN '2022-10-01'::TIMESTAMP AND '2023-02-28'::TIMESTAMP 
        GROUP BY event_month;"""
    )

    purchases = cursor.fetchall()

    cursor.close()
    connection.close

    return purchases


def get_purchase_avg_prices():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        """SELECT date_trunc('day', event_time) AS event_month, avg(price) as total_price
        FROM customers
        WHERE event_type='purchase'
        AND date_trunc('day', event_time) BETWEEN '2022-10-01'::TIMESTAMP AND '2023-02-28'::TIMESTAMP
        GROUP BY event_month;"""
    )

    purchases = cursor.fetchall()

    cursor.close()
    connection.close

    return purchases


def make_chart(x: list[str], y: list[int]) -> None:
    df = pd.DataFrame(data={"dates": x, "customer_count": y})
    plt.plot(df["dates"], df["customer_count"])

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b"))
    plt.ylabel("Number of customers")

    plt.savefig("chart.png")


def make_histogram(x: list[str], y: list[float]) -> None:
    df = pd.DataFrame(data={"dates": x, "prices": y})

    df["dates"] = pd.to_datetime(df["dates"])
    formatted_dates = df["dates"].dt.strftime("%b %Y")

    plt.figure(figsize=(10, 6))
    plt.bar(formatted_dates, df["prices"], color="skyblue")

    plt.ylabel("Price")
    plt.title("Price evolution between October 2022 and January 2023")

    plt.savefig("hist.png")


def make_filled_plot(x: list[str], y: list[float]) -> None:
    df = pd.DataFrame(data={"dates": x, "avg_prices": y})

    plt.plot(df["dates"], df["avg_prices"])
    plt.fill_between(df["dates"], df["avg_prices"])

    plt.savefig("gay.png")


def main():
    # purchases = get_purchases()
    # purchase_dates = [x[0] for x in purchases]
    # customer_count = [y[1] for y in purchases]
    # make_chart(purchase_dates, customer_count)
    #
    # purchases = get_purchase_prices()
    # purchase_dates = [x[0] for x in purchases]
    # purchase_price = [y[1] for y in purchases]
    # make_histogram(purchase_dates, purchase_price)

    purchases = get_purchase_avg_prices()
    purchase_dates = [x[0] for x in purchases]
    purchase_avg_price = [y[1] for y in purchases]
    make_filled_plot(purchase_dates, purchase_avg_price)


if __name__ == "__main__":
    main()
