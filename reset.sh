#!/bin/bash

APPS=casapp

echo "[RESET] Resetting the application..."
rm -rf db.sqlite3
for APP in $APPS; do
	rm -rf $APP/migrations
	python manage.py makemigrations $APP
done
python manage.py migrate
echo "[RESET] Loading users from fixtures"
python manage.py loaddata demo_users.json
