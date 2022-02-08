from django.urls import path
from . import views

urlpatterns = [
path('<str:course>/<str:order>', views.startLive, name='startLive'),
path('join/<str:course>/<str:order>', views.joinLive, name='joinLive'),
path('closeLive/', views.closeLive, name='closeLive'),
path('closepage/', views.closepage, name='closepage'),


]