CREATE DATABASE IF NOT EXISTS passengers_db;
USE passengers_db;

CREATE TABLE IF NOT EXISTS passenger (
    email VARCHAR(255) NOT NULL PRIMARY KEY,
    password VARCHAR(255)
);

LOAD DATA INFILE '/var/lib/mysql-files/data.csv'
INTO TABLE passenger
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;