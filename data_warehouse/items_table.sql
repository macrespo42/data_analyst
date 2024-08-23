CREATE TABLE item (
product_id SERIAL,
category_id VARCHAR(255),
category_code VARCHAR(255),
brand VARCHAR(255));

COPY item(product_id,category_id,category_code,brand)
FROM '/opt/subject/item/item.csv'
DELIMITER ','
NULL as 'null'
CSV HEADER;
