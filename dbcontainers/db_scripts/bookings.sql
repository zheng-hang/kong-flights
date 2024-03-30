CREATE DATABASE IF NOT EXISTS bookings_db;
USE bookings_db;

CREATE TABLE IF NOT EXISTS bookings (
    BID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    PID INT NOT NULL,
    FID VARCHAR(6),
    seatcol VARCHAR(1) NOT NULL,
    seatnum INT NOT NULL
);

LOAD DATA INFILE '/var/lib/mysql-files/data.csv'
INTO TABLE bookings
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;