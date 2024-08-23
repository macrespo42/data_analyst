CREATE TABLE IF NOT EXISTS customers (
    event_time TIMESTAMP,
    event_type VARCHAR(255),
    product_id SERIAL,
    price DECIMAL,
    user_id SERIAL,
    user_session VARCHAR(36)
);

INSERT INTO customers
SELECT * FROM data_2022_dec;

INSERT INTO customers
SELECT * FROM data_2022_nov;

INSERT INTO customers
SELECT * FROM data_2022_oct;

INSERT INTO customers
SELECT * FROM data_2023_jan;
