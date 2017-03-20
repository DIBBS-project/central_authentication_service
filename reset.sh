#!/bin/bash
echo "[RESET] Resetting the application database..."
rm -f db.sqlite3
python manage.py migrate

echo "[RESET] Loading users from fixtures"
python manage.py loaddata demo_users.json
