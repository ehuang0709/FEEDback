import django_heroku
import os
import dj_database_url
from dotenv import load_dotenv, dotenv_values
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

from django.core.management.utils import get_random_secret_key

# Generate a new secret key
SECRET_KEY = get_random_secret_key()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-1!b%v3v%u$(4&ywgj=@nnv*+i6c@(qxyd91&g0)+mqk+nn2#^&')

# DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = ['feedback-whistleblower-313b864b59ec.herokuapp.com', 'localhost', '127.0.0.1']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = []



INSTALLED_APPS = [
    'feedback',
    'allauth',
    'allauth.account',
    'django.contrib.sites',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap5',
    'storages',
]

#google login api configuration (provider), autofill

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online'
        },
        'APP': {
            'client_id': "342520742622-1ufclv2iu5bmte4iipb3mpa2ji2jdrov.apps.googleusercontent.com",
            'secret': "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",
            'key': ''
        }
    }
}


MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



SITE_ID = 2

LOGIN_REDIRECT_URL = 'home'

ROOT_URLCONF = 'mysite.urls'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

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

WSGI_APPLICATION = 'mysite.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require='DATABASE_URL' in os.environ
    )
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'd8aasucfbda64a',
    #     'USER': 'rccbvzdtvxjwwa',
    #     'PASSWORD': '5720dc55807d4b33d6f5d39823c9503738a89be117f9bfc94b6daea3b1603d4a',
    #     'HOST': 'ec2-52-72-109-141.compute-1.amazonaws.com',
    #     'PORT': '5432',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

print("AWS_ACCESS_KEY_ID:", AWS_ACCESS_KEY_ID)
print("AWS_SECRET_ACCESS_KEY:", AWS_SECRET_ACCESS_KEY)

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_S3_SECURE_URLS = True
AWS_QUERYSTRING_AUTH = False

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'feedback-whistleblower.storage_backends.MediaStorage'

django_heroku.settings(locals())