"""
Django settings for aion project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'v+w(2a-rw**_s(0g)%*&9=b!7x@0^*32g(x@b)^2t#%ni)6fz^'

import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'v+w(2a-rw**_s(0g)%*&9=b!7x@0^*32g(x@b)^2t#%ni)6fz^') 

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = [
    'aion.run',
    'aion2-jeff-how.c9users.io', 
    'aionapp.herokuapp.com',
    'ca437448a3004726b8385c4192fda7d9.vfs.cloud9.us-east-1.amazonaws.com',
    '3.227.10.12',
    '0.0.0.0',
    '127.0.0.1'
    ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reservations.apps.ReservationsConfig',
    'analytics',
    'crispy_forms',
    'captcha',
    'django_cron',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Whitenoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'aion.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


'''This may change in the future to: PASSWORD_RESET_TIMEOUT accepting seconds, 
but as of 3/2018 this is an open ticket in Django
'''
PASSWORD_RESET_TIMEOUT_DAYS=1

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# The URL to use when referring to static files (where they will be served from)
STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
#     '/var/www/static/',
# ]

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "staticfiles")
# ]

DATE_INPUT_FORMATS=[
    '%m/%d/%Y',                 # '10/25/2006'
    '%Y-%m-%d', '%m/%d/%y',     # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',    # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',    # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',    # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',    # '25 October 2006', '25 October, 2006'
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/signin/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL ='/signin/'

# Per manage.py check --deploy
X_FRAME_OPTIONS = 'DENY'

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Email Settings using sendgrid
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME', 'aion_app')
# EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', 'mys3cr3tp4ssw0rd')
# EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ACCOUNT_ACTIVATION_DAYS = 3
EMAIL_HOST = 'smtp.yandex.com'
EMAIL_HOST_USER = 'SchoolX.Ar4ikov@yandex.ru'
EMAIL_HOST_PASSWORD = 'W4Hfx0t2Cte8'
EMAIL_PORT = 465
EMAIL_USE_SSL = True

LOGIN_REDIRECT_URL = '/'

DEFAULT_FROM_EMAIL = 'SchoolX <SchoolX.Ar4ikov@yandex.com>'

# Captcha settings
CAPTCHA_IMAGE_SIZE=175,75

# Django_Cron settings
CRON_CLASSES = [
    "reservations.cron.DatabaseCleanup",
]

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# manage.py --deploy report
SECURE_HSTS_SECONDS=518400 # 6 days
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # Heroku requirement
