"""
Test settings for running tests with SQLite instead of PostgreSQL.

This allows us to validate model logic without requiring a running PostgreSQL server.
Note: ArrayField is PostgreSQL-specific, so we use a test override.
"""

from helpinghand.settings import *  # noqa: F401, F403

# Use SQLite for tests — fast and no external dependencies
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
