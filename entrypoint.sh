#!/bin/sh

# Сценарий для инициализации Django проекта в контейнере
# Выполняет миграции и создает суперпользователя

# Применение миграций
echo "Applying migrations..."
python libertypost/manage.py migrate

# Сборка статических файлов
echo "Collecting static files..."
python libertypost/manage.py collectstatic --noinput

# Создание суперпользователя, если не существует
echo "Creating superuser..."
python libertypost/manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME',
                                 '$DJANGO_SUPERUSER_EMAIL',
                                 '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser created.');
else:
    print('Superuser already exists.')
"

# Запуск Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --chdir libertypost --bind 0.0.0.0:8000 libertypost.wsgi:application
