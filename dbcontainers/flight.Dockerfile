FROM mysql:latest

COPY ./db_scripts/flights.sql /docker-entrypoint-initdb.d/flights.sql
