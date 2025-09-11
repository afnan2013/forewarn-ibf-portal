#!/bin/bash
set -e

# PostgreSQL initialization script for FOREWARN IBF Portal
# This runs ONLY when the database is first created

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Set up database for optimal performance
    -- No extensions needed for basic PostgreSQL functionality
    
    -- Log successful initialization
    SELECT 'FOREWARN IBF Database initialized successfully' as status;
    SELECT version() as postgres_version;
EOSQL
