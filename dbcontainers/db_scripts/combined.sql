CREATE DATABASE IF NOT EXISTS smoothairlines;
USE smoothairlines;

CREATE TABLE IF NOT EXISTS flights (
    FID VARCHAR(10) NOT NULL,
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

CREATE TABLE IF NOT EXISTS bookings (
    BID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    EMAIL VARCHAR(255) NOT NULL,
    FID VARCHAR(6),
    seatcol VARCHAR(1) NOT NULL,
    seatnum INT NOT NULL
);

CREATE TABLE IF NOT EXISTS passenger (
    email VARCHAR(255) NOT NULL PRIMARY KEY,
    salt VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS seats (
    fid VARCHAR(255) NOT NULL,
    seatcol VARCHAR(1) NOT NULL,
    seatnum INT NOT NULL,
    available BOOLEAN,
    price DOUBLE,
    seat_class VARCHAR(255),
    PRIMARY KEY (fid,seatcol,seatnum)
);

LOAD DATA INFILE '/var/lib/mysql-files/f_data.csv'
INTO TABLE flights
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/b_data.csv'
INTO TABLE bookings
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/p_data.csv'
INTO TABLE passenger
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/s_data.csv'
INTO TABLE seats
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;