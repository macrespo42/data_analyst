CREATE TABLE customers_tmp (LIKE customers);

INSERT INTO customers_tmp (event_time, event_type, product_id, price, user_id, user_session)
SELECT DISTINCT ON (date_trunc('minute', event_time), event_type, product_id, price, user_id, user_session)
event_time, event_type, product_id, price, user_id, user_session
FROM customers;

DROP TABLE customers;

ALTER TABLE customers_tmp
RENAME TO customers;
