"""
Django settings for OStore project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Sets the project path as a variable to be used below
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__)) + '/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yv&n-@3b@9^!j&0xv&-x59w-@kzd0zay5rkb05)n4!-q2@(a%_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drive',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'OStore.urls'

WSGI_APPLICATION = 'OStore.wsgi.application'

TEMPLATE_DIRS = (
  os.path.join(PROJECT_ROOT, 'templates')
)

ADMINS = (
    ('Omar Syed', 'osyed@andrew.cmu.edu'),
    ('Mikhail Kutsovsky', 'mkutsovs@andrew.cmu.edu'),
)

MANAGERS = ADMINS

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_ROOT + 'db/webapps.db', 
    }
}

ALLOWED_HOSTS = []

AUTH_PROFILE_MODULE= 'drive.MyUser'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

TIME_ZONE = 'US/Eastern'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Absolute path to the directory static files should be collected to.
STATIC_ROOT = PROJECT_ROOT + 'static/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# URL to use if the authentication system requires a user to log in.
LOGIN_URL = '/drive/login'

# Default URL to redirect to after a user logs in.
LOGIN_REDIRECT_URL = '/drive/'
