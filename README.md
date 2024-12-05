# Super Brain

Образовательный сайт для дошкольников и младших классов

### Локальный запуск с Docker compose
- Рядом с файлом manage.py разместить .env файл. Env переменные:
```  
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='proj_db'
DB_USER='pguser'
DB_PASSWORD='pgpassword'
DB_HOST='db'
DB_PORT=5432
SECRET_KEY='some_secret_key'
ALLOWED_HOSTS = '127.0.0.1 localhost'
EMAIL_HOST='mailhog'
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_PORT=1025
EMAIL_USE_TLS='False'
REDIS_URL="redis://redis/1"
CELERY_BROKER_URL="redis://redis/0"
MANAGER_EMAIL="super-brain-manager@example.com"
DEFAULT_FROM_EMAIL="super-brain-manager-noreply@example.com"
```
- В основной папке для создания образа
```console  
docker compose build web
```
- Выполнить команду для миграций
```console  
docker compose run --rm web python manage.py migrate
``` 
- Запустить проект
```console  
docker compose up
```
- Для отображения статических файлов через nginx при DEBUG = False
```console  
docker-compose exec web python manage.py collectstatic --no-input 
```

### Запуск без Docker
- Рядом с файлом manage.py разместить .env файл.
- В основной папке установить и активировать виртуальное окружение
```console  
python -m venv venv
```
```console  
.\venv\Scripts\activate.bat
```

- Установить используемые библиотеки из файла requirements.txt
```console  
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполнить команду для миграций:
```console  
python manage.py migrate  --settings=proj.settings_without_docker
```
- В папке с файлом manage.py выполнить команду для запуска локального сервера:
```console  
python manage.py runserver  --settings=proj.settings_without_docker
```
- Для отображения статических файлов при DEBUG = False
```console  
python manage.py collectstatic --no-input  --settings=proj.settings_without_docker
```

Сайт отобразится по адресу http://127.0.0.1:8000/

### Тестирование проекта
1) Запуск тестов без Docker:

Для запуска всех тестов проекта:
```console  
python manage.py test  --settings=proj.settings_tests
```
Для запуска всех тестов приложения courses:
```console  
python manage.py test courses  --settings=proj.settings_tests
```
Для запуска тестов urls приложения courses:
```console  
python manage.py test courses.tests.tests_urls  --settings=proj.settings_tests
```
Для запуска тестов view-функций приложения courses:
```console  
python manage.py test courses.tests.tests_views  --settings=proj.settings_tests
```
2) Запуск тестов с Docker:

Для запуска всех тестов проекта:
```console  
docker compose run --rm web python manage.py test  --settings=yatube.settings_test
```
Для запуска всех тестов приложения courses:
```console  
docker compose run --rm web python manage.py test courses  --settings=proj.settings_tests
```
Для запуска тестов urls приложения courses:
```console  
docker compose run --rm web python manage.py test courses.tests.tests_urls  --settings=proj.settings_tests
```
Для запуска тестов view-функций приложения courses:
```console  
docker compose run --rm web python manage.py test courses.tests.tests_views  --settings=proj.settings_tests
```
