"""
WSGI config for Helping Hand project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpinghand.settings')

application = get_wsgi_application()
