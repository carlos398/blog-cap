from pathlib import Path
import environ

env = environ.Env()

environ.Env().read_env()


BASE_DIR = Path(__file__).resolve().parent.parent



SQL_LITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


POSTGRES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('PSQL_USER'),
        'PASSWORD': env('PSQL_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}