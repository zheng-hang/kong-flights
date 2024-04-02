CREATE DATABASE IF NOT EXISTS passengers_db;
USE passengers_db;

CREATE TABLE IF NOT EXISTS passenger (
    email VARCHAR(255) NOT NULL PRIMARY KEY,
    salt VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

LOAD DATA INFILE '/var/lib/mysql-files/data.csv'
INTO TABLE passenger
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
