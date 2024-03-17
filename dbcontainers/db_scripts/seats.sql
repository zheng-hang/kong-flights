CREATE DATABASE IF NOT EXISTS seats_db;
USE seats_db;

CREATE TABLE IF NOT EXISTS seats (
    fid VARCHAR(255) NOT NULL,
    seatnum VARCHAR(255) NOT NULL,
    available BOOLEAN,
    price DOUBLE,
    class VARCHAR(255),
    PRIMARY KEY (fid,seatnum)
);

LOAD DATA INFILE '/var/lib/mysql-files/data.csv'
INTO TABLE seats
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;