"""Django settings"""
from . import env, BASE_DIR
from datetime import timedelta
from base.logger import LOGGING

WSGI_APPLICATION = 'base.wsgi.application'

ROOT_URLCONF = 'base.urls'

SECRET_KEY = env('SECRET_KEY', default='django-unsecured-secret-key')

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
    'base',
]

AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('base.permissions.IsAuthenticated',),
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'base.exception_handlers.custom_exception_handler',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'base.middleware.ContentTypeMiddleware',
]

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

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = LOGGING

# --------------------------------- CORS ----------------------------------------------------- #

INSTALLED_APPS.append('corsheaders')
MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = ("http://localhost:3000", "http://127.0.0.1:8080")
CORS_ORIGIN_REGEX_WHITELIST = (r"^https://\w+\.domain_name\.com$",)

# --------------------------------- Authentication -------------------------------------------- #

INSTALLED_APPS += [
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.twitter',
]
AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)
REST_AUTH = {
    'OLD_PASSWORD_FIELD_ENABLED': True,
    'LOGOUT_ON_PASSWORD_CHANGE': True,
    'JWT_AUTH_HTTPONLY': False,
    'USER_DETAILS_SERIALIZER': "user.serializer.UserDetailSerializer",
    'REGISTER_SERIALIZER': 'dj_rest_auth.registration.serializers.RegisterSerializer',
}

# Allauth Settings
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

JWT_AUTHENTICATION_ENABLED = env('JWT_AUTHENTICATION_ENABLED', default=True, cast=bool)
if JWT_AUTHENTICATION_ENABLED:
    INSTALLED_APPS += [
        'rest_framework_simplejwt',
        'rest_framework_simplejwt.token_blacklist',
    ]
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = ('rest_framework_simplejwt.authentication.JWTAuthentication',)
    REST_AUTH['TOKEN_MODEL'] = None
    REST_AUTH['USE_JWT'] = True
    # JWT Settings
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
        'REFRESH_TOKEN_LIFETIME': timedelta(minutes=30),
        'UPDATE_LAST_LOGIN': True,
        'SIGNING_KEY': SECRET_KEY,
        "AUTH_HEADER_TYPES": ("Bearer",),
        "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    }
else:
    INSTALLED_APPS += [
        'rest_framework.authtoken',
    ]
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = ('rest_framework.authentication.TokenAuthentication',)
    TOKEN_LIFETIME = timedelta(minutes=30)

SOCIAL_LOGIN_ENABLED = env('SOCIAL_LOGIN_ENABLED', default=True, cast=bool)
if SOCIAL_LOGIN_ENABLED:
    SOCIALACCOUNT_ADAPTER = 'base.adapter.SocialAccountAdapter'
    SOCIAL_CALLBACK_URL = "http://127.0.0.1"
    SOCIAL_REGISTRATION = False  # To disable the social registration
    SOCIAL_SAME_EMAIL_CONNECT = True  # To check if the user email and the email of the social account is same

# --------------------------------- Cipher Settings -------------------------------------------- #
ENCRYPT = env('ENCRYPT', default=False, cast=bool)
ENCRYPTION_KEY = env('AES_SECRET_KEY', default='')
if ENCRYPT:
    MIDDLEWARE += ['base.middleware.EncryptionMiddleware', ]

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
