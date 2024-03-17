CREATE DATABASE IF NOT EXISTS flights_db;
USE flights_db;

CREATE TABLE IF NOT EXISTS flights (
    FID VARCHAR(6) NOT NULL PRIMARY KEY,
    Airline VARCHAR(255),
    DepartureLoc VARCHAR(255),
    ArrivalLoc VARCHAR(255),
    Date DATE,
    DepartureTime TIME,
    Duration INT,
    Price DOUBLE
);

LOAD DATA INFILE '/var/lib/mysql-files/data.csv'
INTO TABLE flights
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;