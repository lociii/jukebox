import os
import pkgutil
import sys

BASE_DIR = os.path.normpath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

JUKEBOX_STORAGE_PATH = os.path.join(
    os.path.expanduser('~'),
    '.jukebox',
)
if not os.path.exists(JUKEBOX_STORAGE_PATH):
    try:
        os.makedirs(JUKEBOX_STORAGE_PATH, 0750)
    except os.error:
        JUKEBOX_STORAGE_PATH = BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(
            JUKEBOX_STORAGE_PATH,
            'db.sqlite'
        ),
    }
}

SITE_ID = 1

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('de', 'Deutsch'),
    ('en', 'English'),
)
USE_I18N = True
USE_L10N = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
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
    os.path.join(BASE_DIR, 'jukebox_web/templates'),
)

ADMIN_MEDIA_PREFIX = '/static/admin/'

ROOT_URLCONF = 'jukebox.urls'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'jukebox_web/locale'),
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
    'rest_framework',
    'social_auth',
    'south',
    'jukebox_core',
    'jukebox_web',
)

# automatically add jukebox plugins
for item in pkgutil.iter_modules():
    if str(item[1]).startswith('jukebox_'):
        INSTALLED_APPS += (str(item[1]), )

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

sys.path.append(JUKEBOX_STORAGE_PATH)
try:
    from settings_local import *
except ImportError:
    pass
