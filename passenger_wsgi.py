# passenger_wsgi.py
import sys, os

# Replace 'your_project_name' with the name of your Django project folder
sys.path.insert(0, '/home/rentlrdp/dnd_backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dnd_backend.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()