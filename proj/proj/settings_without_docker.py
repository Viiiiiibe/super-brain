from proj.settings import *

# для тестов
SECRET_KEY = 'some_secret_key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

