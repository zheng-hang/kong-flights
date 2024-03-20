FROM mysql:latest

COPY ./db_scripts/seats.sql /docker-entrypoint-initdb.d/seats.sql