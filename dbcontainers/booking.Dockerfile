FROM mysql:latest

COPY ./db_scripts/bookings.sql /docker-entrypoint-initdb.d/bookings.sql