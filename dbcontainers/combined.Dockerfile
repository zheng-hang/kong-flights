FROM mysql:latest

COPY ./db_scripts/combined.sql /docker-entrypoint-initdb.d/combined.sql