# Django settings for artis project.
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Anton', 'antofik@gmail.com'),
)
MANAGERS = ADMINS

SITE_ID = 1
SECRET_KEY = '_^#r&afp;lde=n#r&xmp;%44tr*zy&am#;z^@u=1*$6^2-fergmisw5t&amp;wgzn^'
AUTH_PROFILE_MODULE = 'main.UserProfile'

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'# Language code for this installation. All choices can be found here: http://www.i18nguy.com/unicode/language-identifiers.html
USE_I18N = True # If you set this to False, Django will make some optimizations so as not to load the internationalization machinery.
USE_L10N = True # If you set this to False, Django will not format dates, numbers and calendars according to the current locale.
USE_TZ = True # If you set this to False, Django will not use timezone-aware datetimes.

MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")
MEDIA_URL = '/media/'
CMS_MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_PATH, "static")
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
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

    #Custom applications
    'main',
    'configurator',
    'arena',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)

if USE_I18N:
     TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)

RATINGS_VOTES_PER_IP = 3

SESSION_SAVE_EVERY_REQUEST = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'no-reply@mfst.pro'
EMAIL_HOST_PASSWORD = 'no-reply!!!$'
EMAIL_PORT = 587

THUMBNAIL_DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'django_to_file': {                
            'level': 'DEBUG',
            'class': 'logging.FileHandler', 
            'formatter': 'verbose',         
            'filename': os.path.join(PROJECT_PATH, 'logs', 'django.log') 
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'default': {              
            'handlers': ['django_to_file'], 
            'level': 'INFO',                 
            'propagate': True,
        },     
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Debug toolbar
if DEBUG and False:
     INTERNAL_IPS = ( '127.0.0.1',)
     MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
     INSTALLED_APPS += ('debug_toolbar',)
     DEBUG_TOOLBAR_PANELS = (
         'debug_toolbar.panels.version.VersionDebugPanel', 
         'debug_toolbar.panels.timer.TimerDebugPanel',
         'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
         'debug_toolbar.panels.headers.HeaderDebugPanel',
         'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
         'debug_toolbar.panels.template.TemplateDebugPanel',
         'debug_toolbar.panels.sql.SQLDebugPanel',
         'debug_toolbar.panels.cache.CacheDebugPanel',
         'debug_toolbar.panels.logger.LoggingPanel',
     )
     DEBUG_TOOLBAR_CONFIG = {
         'EXCLUDE_URLS': ('/admin',), 
         'INTERCEPT_REDIRECTS': False,
     }

try:
    from localsettings import *
except ImportError:
    pass


