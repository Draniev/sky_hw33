"""
Django settings for todolist project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = Path(BASE_DIR.parent, '.env', 'data.env')

is_loaded = load_dotenv(ENV_FILE)
if not is_loaded:
    print(
        f'Файл с переменными среды {ENV_FILE} не найден, загружаю из имеющихся...')
#     raise FileNotFoundError(f'ENV File did not found: {ENV_FILE}')

DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PORT = os.environ.get('DB_PORT')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

SECRET = os.getenv('SECRET')
IS_DEBUG = os.getenv('DEBUG')

SECRET_KEY = SECRET

TG_TOKEN = os.environ.get('TG_TOKEN')

DEBUG = IS_DEBUG

ALLOWED_HOSTS = ['*']
# APPEND_SLASH = False


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'social_django',
    'core',
    'goals',
    'bot',
]


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',
    # ),
}
# Настройка для ОAUTH2 приложения, см
# https://python-social-auth.readthedocs.io/en/latest/configuration/django.html
SOCIAL_AUTH_JSONFIELD_ENABLED = True
AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('VK_APP_ID')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('VK_APP_KEY')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'todolist.urls'

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

WSGI_APPLICATION = 'todolist.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/django_static/"
STATIC_ROOT = os.path.join(BASE_DIR, "django_static")

MEDIA_URL = "/django_media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "django_media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/core/login/'
AUTH_USER_MODEL = 'core.User'
