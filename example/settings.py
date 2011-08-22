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

STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    abspath(join(parent, 'templates')),
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'lettuce.django',

    'sample',
    'forms_ext',
)

try:
    import django_jenkins
    PROJECT_APPS = ('forms_ext', 'sample')

    INSTALLED_APPS = INSTALLED_APPS + ('django_jenkins',)
    JENKINS_TASKS = (
        'django_jenkins.tasks.django_tests',
        'django_jenkins.tasks.run_pylint',
        'django_jenkins.tasks.run_pep8',
        'django_jenkins.tasks.run_pyflakes',
        'django_jenkins.tasks.with_coverage',
    )

except ImportError:
    pass
