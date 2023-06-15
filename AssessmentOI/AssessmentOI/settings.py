"""
Django settings for AssessmentOI project.

Generated by 'django-admin startproject' using Django 3.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import dotenv
import django.db.backends.postgresql
# Build paths inside the project like this: BASE_DIR / 'subdir'.
import cx_Oracle
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Add .env variables anywhere before SECRET_KEY
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'assessment',
    'crispy_forms',

    'users.apps.UsersConfig',

    # TODO: #1  The following apps are required for allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # TODO: #2  to use operations on templates
    'mathfilters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AssessmentOI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'users/templates'),
                 BASE_DIR,
                 os.path.join(BASE_DIR, 'assessment/templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                    'template_filters': 'assessment.template_filters',
                }
        },
    },
]

WSGI_APPLICATION = 'AssessmentOI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASE_TYPE = os.environ['DATABASE_TYPE']

DB = {}

if DATABASE_TYPE == 'postgres':
    DB['ENGINE'] = 'django.db.backends.postgresql'
    DB['NAME'] = os.environ['POSTGRESQL_DB']
    DB['USER'] = os.environ['POSTGRESQL_USER']
    DB['PASSWORD'] = os.environ['POSTGRESQL_PASSWORD']
    DB['HOST'] = os.environ['POSTGRESQL_HOST']
    DB['PORT'] = ''

elif DATABASE_TYPE == 'mysql':
    DB['ENGINE'] = 'django.db.backends.mysql'
    DB['NAME'] = os.environ['MYSQL_DB']
    DB['USER'] = os.environ['MYSQL_USER']
    DB['PASSWORD'] = os.environ['MYSQL_PASSWORD']
    DB['HOST'] = os.environ['MYSQL_HOST']
    DB['PORT'] = os.environ['MYSQL_PORT']

elif DATABASE_TYPE == 'oracle':
    if (os.environ('DEPLOYMENT') == 'local'):
        cx_Oracle.init_oracle_client(lib_dir="/Users/stefano/Dropbox/NewDev/AssessmentOI/wallet")
    elif (os.environ('DEPLOYMENT') == 'remote'):
        cx_Oracle.init_oracle_client(lib_dir="home/ubuntu/AssessmentOI/wallet_prod")
    else:
        cx_Oracle.init_oracle_client(lib_dir="home/ubuntu/AssessmentOI/wallet_prod")
    DB['ENGINE'] = 'django.db.backends.oracle'
    DB['NAME'] = os.environ['ORACLE_NAME']
    DB['USER'] = os.environ['ORACLE_USER']
    DB['PASSWORD'] = os.environ['ORACLE_PASSWORD']
    DB['HOST'] = ''
    DB['PORT'] = ''

elif DATABASE_TYPE == 'sqllite':
    DB['ENGINE'] = 'django.db.backends.sqlite3'
    DB['NAME'] = BASE_DIR / 'db.sqlite3'
    DB['USER'] = ''
    DB['PASSWORD'] = ''
    DB['HOST'] = ''
    DB['PORT'] = ''
else:
    DB['ENGINE'] = 'django.db.backends.sqlite3'
    DB['NAME'] = BASE_DIR / 'db.sqlite3'
    DB['USER'] = ''
    DB['PASSWORD'] = ''
    DB['HOST'] = ''
    DB['PORT'] = ''

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    # 'default': { DB }

    'default': {
        'ENGINE': DB['ENGINE'],
        'NAME': DB['NAME'],
        'USER': DB['USER'],
        'PASSWORD': DB['PASSWORD'],
        'HOST': DB['HOST'],
        'PORT': DB['PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

SITE_ID = 1

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# TODO: #6  added for eliminating the username and validate only through emails
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS =True
# ACCOUNT_LOGOUT_ON_GET = True # Added
ACCOUNT_FORMS = {'login': 'users.forms.UserLoginForm'} # Added (to be verified if required)

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# added
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assessment/static'),
    os.path.join(BASE_DIR, 'user/static'),
    os.path.join(BASE_DIR, 'assessment/media'),
    os.path.join(BASE_DIR, 'user/media'),
    # os.path.join(BASE_DIR, '../media/static'),
)


# TODO: #8  Use the new user app
AUTH_USER_MODEL = 'users.User' # new
LOGIN_URL = 'users_login'
# LOGIN_REDIRECT_URL = 'validate_token_view' # this will request the token validation for any user but it should only do it for candidates

LOGIN_REDIRECT_URL = 'home_view'

EMAIL_BACKEND = os.environ['EMAIL_BACKEND']
EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = os.environ['EMAIL_PORT']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
