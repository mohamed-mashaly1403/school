"""
WSGI config for vschool project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os , sys
sys.path.append('/home/mesho/blog/vschool')
sys.path.append('/home/mesho/blog/envl/Lib/site-packages')
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vschool.settings')

application = get_wsgi_application()
# import os, sys
# # add the hellodjango project path into the sys.path
# sys.path.append('<PATH_TO_MY_DJANGO_PROJECT>/hellodjango')
#
# # add the virtualenv site-packages path to the sys.path
# sys.path.append('<PATH_TO_VIRTUALENV>/Lib/site-packages')
#
# # poiting to the project settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hellodjango.settings")
#
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()