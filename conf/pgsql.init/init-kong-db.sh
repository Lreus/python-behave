#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER behave_kong WITH PASSWORD 'kong';
    CREATE DATABASE behave_kong_db;
    GRANT ALL PRIVILEGES ON DATABASE behave_kong_db TO behave_kong;
EOSQL