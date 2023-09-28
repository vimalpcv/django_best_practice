"""Django settings"""
from . import env, BASE_DIR
from datetime import timedelta
from common.logger import LOGGING

SECRET_KEY = env('SECRET_KEY', default='django-unsecured-secret-key')

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    'rest_framework',

    # Internal Apps
    'user',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'common.exception_handlers.custom_exception_handler',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'common.middleware.ContentTypeMiddleware',
]

ROOT_URLCONF = 'common.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'common.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

LOGGING = LOGGING


# --------------------------------- CORS ----------------------------------------------------- #
INSTALLED_APPS.append('corsheaders')
MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = ("http://localhost:3000", "http://127.0.0.1:8080")
CORS_ORIGIN_REGEX_WHITELIST = (r"^https://\w+\.domain_name\.com$",)


# --------------------------------- Authentication -------------------------------------------- #
INSTALLED_APPS += [
    'rest_framework.authtoken',
    'authentication',

    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    'dj_rest_auth',
    'dj_rest_auth.registration',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.twitter',
]
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = ('rest_framework_simplejwt.authentication.JWTAuthentication',)
AUTHENTICATION_CLASSES = ('dj_rest_auth.authentication.AllAuthJWTAuthentication', )
AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)
REST_AUTH = {
    'OLD_PASSWORD_FIELD_ENABLED': False,
    'LOGOUT_ON_PASSWORD_CHANGE': False,
    'JWT_AUTH_HTTPONLY': False,
    'USER_DETAILS_SERIALIZER': "user.serializer.UserDetailSerializer",
    'REGISTER_SERIALIZER': 'dj_rest_auth.registration.serializers.RegisterSerializer',
    'USE_JWT': True,  # JWT Settings
}

# Allauth Settings
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
CALLBACK_URL = "http://127.0.0.1"
# To disable the social registration
SOCIALACCOUNT_ADAPTER = 'authentication.adapter.SocialAccountAdapter'


# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=100),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'UPDATE_LAST_LOGIN': True,
    'SIGNING_KEY': SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}


# --------------------------------- Cipher Settings -------------------------------------------- #
ENCRYPT = env('ENCRYPT', default=False, cast=bool)
ENCRYPTION_KEY = env('AES_SECRET_KEY', default='')
if ENCRYPT:
    MIDDLEWARE += ['common.middleware.EncryptionMiddleware', ]


# --------------------------------- API Documentation Settings --------------------------------- #
INSTALLED_APPS += ['drf_spectacular', ]
SPECTACULAR_SETTINGS = {
    'TITLE': 'Best Practice Django Syntax',
    'DESCRIPTION': 'This project serves as a comprehensive guide and template for building robust and scalable web '
                   'APIs using Django and Django Rest Framework (DRF). It embodies best practices for code '
                   'organization, authentication methods, efficient logging, and thorough documentation. '
                   'When embarking on a Django project, this resource will help to kickstart API development '
                   'with confidence.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    "SERVERS": [
        {"url": "http://127.0.0.1:8001", "description": "Development server"},
        {"url": "http://127.0.0.1:8001", "description": "Staging server"},
    ],
}
