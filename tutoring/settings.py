# settings.py for Django Project
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lg7rm)52fow)9)ud08l9@+wj70r#-*)e2cs!n7*kcr584$_l3n'
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', 'pk_test_51PPYhKKmcdX5hfexZoWXMaCyow4EvjY6zyztJdsp5mJbVYuFkVT7Rj4GA7gdT6K64njxudFtWjRDu8W1vO8RAU7V00E0prD9Wi')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_51PPYhKKmcdX5hfexAhNnhOzvKB1g2OXOdJvgUzN9Nh20igw3x95Fzuot3ERqTQYVNMagQFhgJTCArhxeHL4LGGbb00xdBioarF')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allowed hosts defines which host/domain names that this Django site can serve.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# CSRF Trusted Origins adds the HTTP origins that are trusted to send the CSRF token.
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000','tutoring1-2a2a70348a6b.herokuapp.com','northwalestutoring.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # Your custom app
    'rest_framework',  # Django REST Framework
    'django.contrib.humanize',
    'schedule',  # Include the schedule app
    'payments',  # Include the payments app

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

ROOT_URLCONF = 'tutoring.urls'

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# Add this to specify where users should be redirected after logging in successfully
LOGIN_REDIRECT_URL = '/'

# Optional: specify where to go after logging out
LOGOUT_REDIRECT_URL = '/'

WSGI_APPLICATION = 'tutoring.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'collected_static'

# Media files
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


# Add this to specify where users should be redirected after logging in successfully
LOGIN_REDIRECT_URL = '/'

# Optional: specify where to go after logging out
LOGOUT_REDIRECT_URL = '/'
# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# settings.py


# Payment settings
PAYMENT_HOST = 'localhost'
PAYMENT_USES_SSL = False
PAYMENT_MODEL = 'core.Payment'  # Ensure this is correctly pointing to your Payment model
PAYMENT_VARIANTS = {
    'default': ('payments.dummy.DummyProvider', {})
}
