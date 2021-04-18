python manage.py migrate
python manage.py loaddata style_fixture
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME || return 0