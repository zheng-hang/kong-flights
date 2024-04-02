CREATE DATABASE IF NOT EXISTS flights_db;
USE flights_db;

CREATE TABLE IF NOT EXISTS flights (
    FID VARCHAR(6) NOT NULL,
    Airline VARCHAR(255),
    DepartureLoc VARCHAR(255),
    ArrivalLoc VARCHAR(255),
    Date DATE NOT NULL,
    DepartureTime TIME,
    Duration INT,
    Price FLOAT,
    DepAirportCode VARCHAR(3),
    ArrAirportCode VARCHAR(3),
    PRIMARY KEY (fid,Date)
);

LOAD DATA INFILE '/var/lib/mysql-files/data.csv'
INTO TABLE flights
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;