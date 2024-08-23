CREATE TABLE IF NOT EXISTS :table (
event_time TIMESTAMP,
event_type VARCHAR(255),
product_id SERIAL,
price DECIMAL,
user_id SERIAL,
user_session VARCHAR(36));


COPY :table (event_time,event_type,product_id,price,user_id,user_session)
FROM :'tablepath'
DELIMITER ','
CSV HEADER;
