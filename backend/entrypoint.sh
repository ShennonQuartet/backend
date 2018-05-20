#!/bin/sh
set -e

python3 backend/manage.py migrate

./backend/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin') if not User.objects.filter(username='admin') else None;"

exec "$@"