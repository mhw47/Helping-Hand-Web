"""
WSGI config for Helping Hand project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpinghand.settings')

import sys
import traceback

_startup_error = None
try:
    _application = get_wsgi_application()
except Exception as e:
    _startup_error = traceback.format_exc()
    if not _startup_error or _startup_error.strip() == "NoneType: None":
        _startup_error = f"Exception: {str(e)} ({type(e).__name__})"

def application(environ, start_response):
    if _startup_error:
        start_response('500 Internal Server Error', [('Content-type', 'text/plain; charset=utf-8')])
        return [f"STARTUP ERROR:\n{_startup_error}".encode('utf-8')]
    try:
        return _application(environ, start_response)
    except Exception as e:
        err = traceback.format_exc()
        if not err or err.strip() == "NoneType: None":
            err = f"Exception: {str(e)} ({type(e).__name__})"
        # Note: if start_response was already called, this might still fail, 
        # but Vercel will catch the WSGI violation. We try our best.
        try:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain; charset=utf-8')])
        except:
            pass
        return [f"RUNTIME ERROR:\n{err}".encode('utf-8')]

app = application
