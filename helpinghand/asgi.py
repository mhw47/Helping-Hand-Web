"""
ASGI config for Helping Hand project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpinghand.settings')

application = get_asgi_application()
