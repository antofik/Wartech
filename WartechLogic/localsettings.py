# Django settings for artis project.
import os

DEBUG = True

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': os.path.join(PROJECT_PATH, "sqldb.lite"),                      # Or path to database file if using sqlite3.
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'logic.wartech',
        'USER': 'root',
        'PASSWORD': 'root',
        #'USER': 'wartech.logic',
        #'PASSWORD': 'fda34k2;dSA#%%435rfda2S',
        'HOST': 'logic.wartech.pro',
        'PORT': '',
        #'OPTIONS': {'read_default_file': os.path.join(PROJECT_PATH, 'mysql.cnf'),},
    }
}
