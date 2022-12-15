"""
WSGI config for vschool project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import django
from django.core.handlers.wsgi import WSGIHandler


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vschool.settings.production')
django.setup(set_prefix=False)
application = WSGIHandler()
# import os
# import django
# from django.core.handlers.wsgi import WSGIHandler
#
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eisentask.settings.production")
# django.setup(set_prefix=False)
#
# application = WSGIHandler()