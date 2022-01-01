from django.urls import path
from . import views
urlpatterns = [
path('', views.TeacherDashboard, name='TeacherDashboard'),
path('teacherProfile/', views.teacherProfile, name='teacherProfile'),
path('Teachercomplains/', views.Teachercomplains, name='Teachercomplains'),
path('TeacherOrders/', views.TeacherOrders, name='TeacherOrders'),
path('TeacherActiveOrders/', views.TeacherActiveOrders, name='TeacherActiveOrders'),
path('ReceivedInstallments/', views.ReceivedInstallments, name='ReceivedInstallments'),
path('AskForWithdraw/', views.AskForWithdraw, name='AskForWithdraw'),
path('Teacheredit_profile/', views.Teacheredit_profile, name='Teacheredit_profile'),


]