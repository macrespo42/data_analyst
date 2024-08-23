CREATE TABLE item_dedup (LIKE item);

INSERT INTO item_dedup (product_id, category_id, category_code, brand)
SELECT DISTINCT ON (product_id) product_id, category_id, category_code, brand
FROM item;

DROP TABLE item;

ALTER TABLE item_dedup
RENAME TO item;

CREATE TABLE customers_left_joined_item (
  event_time TIMESTAMP,
  event_type VARCHAR(255),
  product_id SERIAL,
  price DECIMAL,
  user_id SERIAL,
  user_session VARCHAR(36),
  item_category_id VARCHAR(255),
  item_category_code VARCHAR(255),
  item_brand VARCHAR(255)
);

INSERT INTO customers_left_joined_item (
  event_time,
  event_type,
  product_id,
  price,
  user_id,
  user_session,
  item_category_id,
  item_category_code,
  item_brand
)
SELECT customers.event_time, 
  customers.event_type,
  customers.product_id,
  customers.price,
  customers.user_id,
  customers.user_session,
  item.category_id as item_category_id,
  item.category_code as item_category_code,
  item.brand as item_brand
FROM customers
LEFT JOIN item ON customers.product_id = item.product_id;

drop table customers;

ALTER TABLE customers_left_joined_item
RENAME TO customers;
