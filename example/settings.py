# app lives in a directory above our example
# project so we need to make sure it is findable on our path.
import sys
from os.path import abspath, dirname, join
parent = abspath(dirname(__file__))
grandparent = abspath(join(parent, '..'))
for path in (grandparent, parent):
    if path not in sys.path:
        sys.path.insert(0, path)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'example.db',
    }
}

SECRET_KEY = 'abcahfdkafdaksfdj93243'

STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (abspath(join(parent, 'templates')), )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

INTERNAL_IPS = ('127.0.0.1', )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django_nose',
    'sample',
    'forms_ext',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
