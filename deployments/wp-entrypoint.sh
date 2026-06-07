#!/bin/bash
set -e

# Start Apache in background
apache2-foreground &

# Wait for DB
until mysqladmin ping -h "$WORDPRESS_DB_HOST" --silent; do
  sleep 1
done

# Import backup only if DB is empty
if [ "$(wp db tables --allow-root 2>/dev/null | wc -l)" -eq 0 ]; then
  echo "Importing honeypot backup..."
  wp import /import/vulnsite.wpress --allow-root
fi

wait