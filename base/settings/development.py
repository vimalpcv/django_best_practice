from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

#  --------------------------------- Database Settings ----------------------------------------- #
# ____________SQLite____________ #
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ____________PostgreSQL____________ #
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': env('DB_HOST', default='localhost'),
#         'PORT': env('DB_PORT', default=5432),
#         'NAME': env('DB_NAME', default='django_best_practice'),
#         'USER': env('DB_USER', default='postgres'),
#         'PASSWORD': env('DB_PASSWORD', default='123'),
#
#     }
# }

# __________MYSQL and MariaDB____________ #
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST': env('DB_HOST', default='localhost'),
#         'PORT': env('DB_PORT', default=3306),
#         'NAME': env('DB_NAME', default='django_best_practice'),
#         'USER': env('DB_USER', default='root'),
#         'PASSWORD': env('DB_PASSWORD', default=''),
#     }
# }


# ____________Oracle____________ #
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.oracle',
#         'HOST': env('DB_HOST', default='localhost'),
#         'PORT': env('DB_PORT', default=1521),
#         'NAME': env('DB_NAME', default='django_best_practice'),
#         # 'NAME': 'host.com:1521/dbname',
#         'USER': env('DB_USER', default='system'),
#         'PASSWORD': env('DB_PASSWORD', default='oracle'),
#     }
# }


# Password validation


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True