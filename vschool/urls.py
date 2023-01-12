from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path,include

from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    path('mesho/', admin.site.urls),
    path('',views.home, name='home'),
    path('courses/',include('courses.urls')),
    path('users/',include('users.urls')),
    path('Notifs/',include('Notifs.urls')),
    path('orders/',include('orders.urls')),
    path('Teachers/',include('Teachers.urls')),
    path('live/',include('live.urls')),
    path('admin/',include('admin_honeypot.urls', namespace='admin_honeypot')),


)+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)


handler404 = 'vschool.views.handler404'