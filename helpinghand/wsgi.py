"""
WSGI config for Helping Hand project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpinghand.settings')

try:
    application = get_wsgi_application()
except Exception as e:
    import traceback
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [traceback.format_exc().encode('utf-8')]

app = application  # Required by Vercel serverless functions
