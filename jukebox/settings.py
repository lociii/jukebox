import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + '/db.sqlite',
    }
}

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('de', 'Deutsch'),
    ('en', 'English'),
)
USE_I18N = True
USE_L10N = True

STATIC_ROOT = ''
STATIC_URL = '/static/'
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_DIRS = (
    BASE_DIR + "/jukebox_web/templates"
)

ADMIN_MEDIA_PREFIX = '/static/admin/'

ROOT_URLCONF = 'jukebox.urls'

LOCALE_PATHS = (
    BASE_DIR + '/jukebox_web/locale',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'djangorestframework',
    'social_auth',
    'jukebox_core',
    'jukebox_shout',
    'jukebox_mpg123',
    'jukebox_web',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'social_auth.context_processors.social_auth_by_type_backends',
)

LOGIN_URL          = '/login'
LOGIN_ERROR_URL    = '/login/error'
LOGIN_REDIRECT_URL = '/'

SESSION_TTL = 300

from settings_local import *