from django.urls import path

from Notifs import views


urlpatterns = [



    path('<noti_id>/delete', views.DeleteNotification, name='delete-notification')
]

