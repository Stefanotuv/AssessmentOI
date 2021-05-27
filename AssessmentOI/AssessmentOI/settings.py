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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
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
# SECRET_KEY = 'django-insecure-*buuu-oaji#2m^oi#@(^^2c)d_s%3u5e5#rbxz^uiu_28mrw_@'
SECRET_KEY = os.environ['SECRET_KEY']
HOSTNAME = os.environ['HOSTNAME']
POSTGRESQL_DB = os.environ['POSTGRESQL_DB']
POSTGRESQL_USER = os.environ['POSTGRESQL_USER']
POSTGRESQL_PASSWORD = os.environ['POSTGRESQL_PASSWORD']
POSTGRESQL_HOST = os.environ['POSTGRESQL_HOST']
POSTGRESQL_PORT =  os.environ['POSTGRESQL_PORT']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [HOSTNAME,'*']


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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': POSTGRESQL_DB,
#         'USER': POSTGRESQL_USER,
#         'PASSWORD': POSTGRESQL_PASSWORD,
#         'HOST': POSTGRESQL_HOST,
#         'PORT': POSTGRESQL_PORT,
#     }
# }


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
STATIC_ROOT = os.path.join(BASE_DIR, 'static/') # added for prod
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# added
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, 'static'),
#    os.path.join(BASE_DIR, '../media/static'),
)


# TODO: #8  Use the new user app
AUTH_USER_MODEL = 'users.User' # new
LOGIN_URL = 'users_login'

# change the redirection for the token it was for the previous iteration
# LOGIN_REDIRECT_URL = 'validate_token_view'

LOGIN_REDIRECT_URL = 'home_view'
