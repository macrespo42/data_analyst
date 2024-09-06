from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


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


def get_customers_data() -> list[tuple[Any, ...]]:
    connection = connect_db()

    cursor = connection.cursor()
    cursor.execute(
        """SELECT user_id,
            SUM(price) AS total_spent,
            COUNT(DISTINCT item_category_id) AS categories,
            COUNT(event_type) AS total_events
            FROM customers
            GROUP BY user_id;"""
    )

    return cursor.fetchall()


def get_dataset() -> pd.DataFrame:
    raw_data = get_customers_data()

    total_spents = [float(spent[1]) for spent in raw_data]
    categories = [float(category[2]) for category in raw_data]
    event_types = [float(event_type[2]) for event_type in raw_data]

    data = {
        "total_spents": total_spents,
        "categories": categories,
        "event_types": event_types,
    }

    df = pd.DataFrame(data=data)
    return df


def compute_elbow(df: pd.DataFrame) -> list[Any]:
    scaler = StandardScaler()

    df_scaled = scaler.fit_transform(df)
    inertias = []

    k_values = range(1, 11)
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(df_scaled)
        inertias.append(kmeans.inertia_)

    return inertias


def main() -> None:
    df = get_dataset()
    inertias = compute_elbow(df)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, 11), inertias, marker="o")
    plt.title("The Elbow Method")
    plt.xlabel("Numbers of cluster")
    plt.ylabel("Inertia")
    plt.savefig("inertia.png")


if __name__ == "__main__":
    main()
