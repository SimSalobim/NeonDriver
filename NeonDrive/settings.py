import os
import sys

from dotenv import load_dotenv
from pathlib import Path
import environ
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()
load_dotenv()

env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print(f"ℹ️ {env_path} doesn't exist - using environment variables")

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://neondriver_user:qTwJEDfdqYL0xW5WkmnSbq6dQSYD9Bh5@dpg-d11ifqodl3ps73cr2bng-a.frankfurt-postgres.render.com/neondriver')

# Конфигурация основной базы данных
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

if not DATABASES['default']['PORT']:
    DATABASES['default']['PORT'] = '5432'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '9dn&kx=fnyu5t0xmvcim*g#_t=&=_5!f2v_o*h$8crim+&1tzf')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['neondriver.onrender.com']

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'channels_postgres',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'NeonDrive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'main.context_processors.car_request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
            "prefix": "neondrive",  # Добавьте уникальный префикс
        },
    },
}
# Добавим диагностический вывод
print(f"Database URL: {DATABASE_URL}")
print(f"Channel layers config: {CHANNEL_LAYERS}")
print(f"Channel layer backend: {CHANNEL_LAYERS['default']['BACKEND']}")

WSGI_APPLICATION = 'NeonDrive.wsgi.application'

ASGI_APPLICATION = 'NeonDrive.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Для collectstatic
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Ваши исходные статические файлы



# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

CSRF_TRUSTED_ORIGINS = [
    'https://neondriver.onrender.com',
    'http://localhost:8000'
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

if 'runserver' not in sys.argv and 'collectstatic' not in sys.argv:
    os.environ.setdefault('RUN_INIT', 'true')
