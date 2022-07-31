from django.urls import path
from . import views


urlpatterns = [
# path('', courseListView.as_view(), name='courses'),
path('', views.courses, name='courses'),
path('courseDetails/<str:course_name>/', views.courseDetails, name='courseDetails'),
path('search', views.search, name='search'),
path('pricing', views.pricing, name='pricing'),


]