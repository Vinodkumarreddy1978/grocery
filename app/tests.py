import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocerystore.settings')
django.setup()

from django.db import connection
# Your code here
