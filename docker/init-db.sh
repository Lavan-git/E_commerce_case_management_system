#!/usr/bin/env bash

set -e

echo "Waiting for PostgreSQL..."

until pg_isready \
    -h postgres \
    -U "$POSTGRES_USER" \
    -d "$POSTGRES_DB"
do
    sleep 1
done

echo "PostgreSQL is ready."

echo "Applying database schema..."

for file in /schema/*.sql
do
    echo "Applying $file"

    PGPASSWORD="$POSTGRES_PASSWORD" \
    psql \
        -h postgres \
        -U "$POSTGRES_USER" \
        -d "$POSTGRES_DB" \
        -f "$file"
done

echo "Loading seed data..."

PGPASSWORD="$POSTGRES_PASSWORD" \
psql \
    -h postgres \
    -U "$POSTGRES_USER" \
    -d "$POSTGRES_DB" \
    -f /seeds/001_demo_data.sql

echo "Database initialization completed."