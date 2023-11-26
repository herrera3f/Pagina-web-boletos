"""
Django settings for Django project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0##s)w16#bw3(c+p(xf%z!l8cj-nv7$l8*qwsyc+7j%6k61^%='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'Reserva'
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

ROOT_URLCONF = 'Django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Reserva','templates')],
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

WSGI_APPLICATION = 'Django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bd_brandon',  # Reemplaza 'mydb' con el nombre de tu base de datos MySQL
        'USER': 'herrera3f',  # Reemplaza 'mysql_user' con el nombre de usuario de MySQL
        'PASSWORD': 'Bsmh.7700',  # Reemplaza 'mysql_password' con la contraseña de MySQL
        'HOST': 'db4free.net',  # Reemplaza 'localhost' con la dirección de tu servidor MySQL
        'PORT': '3306',  # Reemplaza '3306' con el puerto de tu servidor MySQL
    },
    'django_sessions': {
        'ENGINE': 'django.db.backends.mysql',  # Ajusta según tu motor de base de datos
        'NAME': 'bd_brandon',
        'USER': 'herrera3f',
        'PASSWORD': 'Bsmh.7700',
        'HOST': 'db4free.net',
        'PORT': '3306',
    },
}


MONGODB_DATABASES = {
    'default': {
        'NAME': 'User',  # Nombre de tu base de datos MongoDB
        'HOST': 'mongodb+srv://benjaminmartinez29:Martinez890@User.bhz2ags.mongodb.net/User?retryWrites=true&w=majority',  # URI de conexión a MongoDB
    }
}



RABBITMQ_HOST = 'localhost'  # Reemplaza con la dirección de tu servidor RabbitMQ si es diferente

RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_PORT = 5672  # El puerto predeterminado de RabbitMQ


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'Django/static')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Desactiva el uso de la base de datos para sesiones
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # Puedes cambiarlo a otro engine según tus necesidades
SESSION_COOKIE_NAME = 'tu_nombre_de_cookie'  # Establece un nombre de cookie personalizado
SESSION_COOKIE_AGE = 1209600  # Duración de la cookie en segundos (por ejemplo, 2 semanas)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = False  # Establece en True en producción si usas HTTPS
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # Puedes cambiarlo a otro engine según tus necesidades

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'brandonstibenmarinherrera@gmail.com'
EMAIL_HOST_PASSWORD = 'asft dcwt lvys fxaw'
