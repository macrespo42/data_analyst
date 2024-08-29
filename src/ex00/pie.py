import matplotlib.pyplot as plt
import psycopg2


def get_event_type_count():
    host = "db"
    port = "5432"
    dbname = "piscineds"
    user = "macrespo"
    password = "mysecretpassword"
    try:
        connection = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=user, password=password
        )
        cursor = connection.cursor()
        cursor.execute(
            "SELECT event_type, count(event_type) FROM customers GROUP BY event_type;"
        )
        event_type_count = cursor.fetchall()

        cursor.close()
        connection.close

        return event_type_count

    except Exception as e:
        print("Erreur lors de la connection a postgres: ", e)
        exit(1)


def make_pie_chart(label: list[str], count: list[int]) -> None:
    plt.pie(count, labels=label, autopct="%1.1f%%")
    plt.savefig("pie.png")


def main():
    event_type_count = get_event_type_count()
    labels = [label[0] for label in event_type_count]
    counts = [count[1] for count in event_type_count]
    make_pie_chart(labels, counts)


if __name__ == "__main__":
    main()
