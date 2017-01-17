#! /bin/bash

APPS=central_authentication_service
PROVIDER="github"
CLIENT_ID="3de92b2457a86df13ab5"
CLIENT_SECRET="837a924ce7cc4bc9cc7db872454db38782d921a0"

echo "[RESET] Resetting the application..."
rm -rf tmp
rm -rf db.sqlite3
for APP in $APPS; do
	rm -rf $APP/migrations
	python manage.py makemigrations $APP
done
python manage.py migrate
echo "[RESET] Creating superuser 'admin' with password 'pass'..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell
echo "[RESET] Creating github social app"
echo "from allauth.socialaccount.models import SocialApp, Site;site = Site.objects.all()[0];social_app = SocialApp();social_app.save();social_app.provider = '$PROVIDER';social_app.name = 'GitHubSocialApp';social_app.client_id = '$CLIENT_ID';social_app.secret = '$CLIENT_SECRET';social_app.sites = [site];social_app.save()" | python manage.py shell
