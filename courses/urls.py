from django.urls import path
from . import views

urlpatterns = [
path('', views.courses, name='courses'),
path('courseDetails/<str:course_name>/', views.courseDetails, name='courseDetails'),
]