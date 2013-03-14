import os
import sys

path = os.path.normpath(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jukebox.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
