CREATE DATABASE IF NOT EXISTS seats_db;
USE seats_db;

CREATE TABLE IF NOT EXISTS seats (
    fid VARCHAR(255) NOT NULL,
    seatcol VARCHAR(1) NOT NULL,
    seatnum INT NOT NULL,
    available BOOLEAN,
    price DOUBLE,
    seat_class VARCHAR(255),
    PRIMARY KEY (fid,seatcol,seatnum)
);

LOAD DATA INFILE '/var/lib/mysql-files/data.csv'
INTO TABLE seats
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;