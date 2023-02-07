from django.urls import path
from . import views

urlpatterns = [
path('<str:course>/<str:order>/<int:classno>', views.startLive, name='startLive'),
path('join/<str:course>/<str:order>/<int:classno>', views.joinLive, name='joinLive'),
path('closeLive/', views.closeLive, name='closeLive'),
path('closepage/', views.closepage, name='closepage'),


]