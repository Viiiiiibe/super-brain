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

Сайт отобразится по адресу http://127.0.0.1:8000/
