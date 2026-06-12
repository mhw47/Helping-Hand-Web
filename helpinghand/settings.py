"""
Django settings for Helping Hand project.

Healthcare marketplace — Django + HTMX + PostgreSQL
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Security ─────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-dev-key-change-in-production-!@#$%^&*()'
)

DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') + ['.vercel.app']

# ─── Applications ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'django_extensions',

    # Local
    'core.apps.CoreConfig',
]

# ─── Middleware ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', # adds a security layer
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Handles static assets production-side
    'django.contrib.sessions.middleware.SessionMiddleware', # stores session
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # For Authentication
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'helpinghand.urls'

# ─── Templates ─────────────────────────────────────────────────────────────────
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

WSGI_APPLICATION = 'helpinghand.wsgi.application'

import dj_database_url

# ─── Database ──────────────────────────────────────────────────────────────────
# Use Vercel/Supabase connection string if available
db_url = os.getenv('POSTGRES_URL') or os.getenv('DATABASE_URL')

if db_url:
    # Only require SSL for non-SQLite databases
    is_sqlite = db_url.startswith('sqlite')
    config = dj_database_url.parse(db_url, conn_max_age=600, ssl_require=not is_sqlite)
    
    # Vercel's Supabase Integration adds custom query parameters that crash psycopg2.
    # We must remove them from the OPTIONS dictionary before Django connects.
    if 'OPTIONS' in config:
        config['OPTIONS'].pop('supa', None)
        config['OPTIONS'].pop('pgbouncer', None)
        config['OPTIONS'].pop('connection_limit', None)
        config['OPTIONS'].pop('pool_timeout', None)
        # SQLite does not support sslmode
        if is_sqlite:
            config['OPTIONS'].pop('sslmode', None)

    DATABASES = {
        'default': config
    }
elif os.getenv('VERCEL') == '1' and not os.getenv('DB_HOST'):
    # Fallback to SQLite during Vercel build step (if not using test_settings)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Local development or traditional Docker/Env configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'helpinghand'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'mohmaya420'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'OPTIONS': {
                'connect_timeout': 5,
                'sslmode': 'require',
            },
        }
    }

# ─── Custom User Model ────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'core.User'

# ─── Password Validation ──────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Authentication ───────────────────────────────────────────────────────────
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ─── Internationalization ─────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ─── Static Files ─────────────────────────────────────────────────────────────
STATIC_URL = '/static/'  # Added leading slash required by Vercel routing
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles_build' / 'static'

# ─── Media Files ───────────────────────────────────────────────────────────────
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── Default Primary Key ──────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
