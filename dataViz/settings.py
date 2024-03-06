"""
Django settings for dataViz project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import pathlib
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.utils import timezone

from secret.secret import POSTGRES__PASS, DJANGO_SECRET_KEY, IS_PRODUCTION, POSTGRES__PORT

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_PRODUCTION

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "llindholm.com"]


# Application definition

INSTALLED_APPS = [
    'dataViz.apps.AdminConfig',
    'users',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "crispy_forms",
    "crispy_bootstrap5",
    "dashboard",
    "data",
    "tags",
    # "reversion",
    "energy_utils",
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail',
    'rest_framework',
    'wagtail.api.v2',
    'modelcluster',
    'taggit',
    'wagtail_home',
    'wagtail.admin',
    'study_notes',
    'wagtailcodeblock',
    'stocks',
    'time_booking',
    'personal_site_content'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

]

ROOT_URLCONF = 'dataViz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'dataViz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": 'django.db.backends.postgresql',
        "NAME": 'dataViz',
        "USER": 'postgres',
        "PASSWORD": POSTGRES__PASS,
        "HOST": "localhost",
        "PORT": POSTGRES__PORT
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "users.User"

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'sv-swe'

TIME_ZONE = 'Europe/Stockholm'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (
    BASE_DIR.joinpath('static/'),  # or project_static, whatever
)

STATIC_ROOT = os.path.join(BASE_DIR, "static_root/")
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Base url to serve media files
MEDIA_URL = '/media/'

# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


BASE_CONTEXT = {"email": "ludvig@llindholm.com",
                "time": timezone.now,
                "brand_name": "Yapity",
                "MEDIA_URL": MEDIA_URL,
                "themes": ["light", "dark", "cupcake", "bumblebee", "emerald", "corporate", "synthwave", "retro", "cyberpunk", "valentine", "halloween", "garden", "forest", "aqua",
                           "lofi", "pastel", "fantasy", "wireframe", "black", "luxury", "dracula", "cmyk", "autumn", "business", "acid", "lemonade", "night", "coffee", "winter", "dim", "nord", "sunset"]
                }

DATA_FILES = BASE_DIR.joinpath("DEVELOPMENT_STORAGE")
WAGTAIL_SITE_NAME = 'Yapity'
WAGTAILADMIN_BASE_URL = "llindholm.com/cms"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

WAGTAIL_CODE_BLOCK_LANGUAGES = (
    ('bash', 'Bash/Shell'),
    ('css', 'CSS'),
    ('diff', 'diff'),
    ('html', 'HTML'),
    ('javascript', 'Javascript'),
    ('json', 'JSON'),
    ('python', 'Python'),
    ('scss', 'SCSS'),
    ('yaml', 'YAML'),
    ('scala', 'Scala'),
    ('rust', 'Rust'),
    ('cpp', 'C++'),
    ('haskell', 'Haskell'),
    ('java', 'Java')
)
WAGTAIL_CODE_BLOCK_LINE_NUMBERS = True
WAGTAIL_CODE_BLOCK_COPY_TO_CLIPBOARD = True
WAGTAIL_CODE_BLOCK_THEME = 'okaidia'

LOGIN_URL = "/users/login"
WAGTAIL_FRONTEND_LOGIN_URL = LOGIN_URL
PASSWORD_REQUIRED_TEMPLATE = 'wagtail_home/password_required.html'


APPEND_SLASH = True
WAGTAILADMIN_STATIC_FILE_VERSION_STRINGS = True
if IS_PRODUCTION:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn="https://0fcbf47fd99946289516f84646ba90a8@o1322592.ingest.sentry.io/6627281",
        integrations=[
            DjangoIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.01,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
