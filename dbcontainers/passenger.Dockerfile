FROM mysql:latest

COPY ./db_scripts/passengers.sql /docker-entrypoint-initdb.d/passengers.sql