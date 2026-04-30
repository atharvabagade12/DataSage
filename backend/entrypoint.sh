#!/bin/bash
set -e

echo "🚀 DataSage Backend Entrypoint"

# Extract database connection details from DATABASE_URL
# Handles both formats: host:port/db AND host/db (no port)
DB_HOST="${DATABASE_URL#*@}"      # strips everything up to @  -> host:port/db OR host/db
DB_HOST="${DB_HOST%%/*}"          # strips /db and beyond       -> host:port OR host
DB_HOST="${DB_HOST%%:*}"          # strips :port                -> host
DB_USER="${DATABASE_URL#*://}"
DB_USER="${DB_USER%%:*}"
DB_NAME="${DATABASE_URL##*/}"

echo "⏳ Waiting for PostgreSQL at $DB_HOST (database: $DB_NAME)..."

# Wait for PostgreSQL to be ready
until pg_isready -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; do
  echo "   PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "✅ PostgreSQL is ready!"

# Run database migrations/initialization
echo "🔧 Running database migrations..."
python init_db.py

if [ $? -eq 0 ]; then
    echo "✅ Database initialized successfully!"
else
    echo "⚠️  Database initialization had warnings (may already exist)"
fi

echo "🎯 Starting FastAPI application..."

# Execute the main command (passed as arguments to this script)
exec "$@"
