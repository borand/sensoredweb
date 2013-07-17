from .base import *
DEBUG = False
# print "Using testing settings"
# print "Top directoyr: " + root("../..")
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = root('..')
TEST_DISCOVER_ROOT = root('..')
TEST_DISCOVER_PATTERN = 'test_*'

LOGGING['loggers']['app']['level'] = 'INFO'