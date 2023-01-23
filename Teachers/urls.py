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
path('TeacherCourseDetails/<int:order_id>', views.TeacherCourseDetails, name='TeacherCourseDetails'),
path('RejectCourse/<int:order_id>/', views.RejectCourse, name='RejectCourse'),
path('submit_courseUrl/<int:order_id>/', views.submit_courseUrl, name='submit_courseUrl'),
path('submit_courseMaterial/<int:order_id>/', views.submit_courseMaterial, name='submit_courseMaterial'),
path('lessonDone/<int:order_id>/', views.lessonDone, name='lessonDone'),
path('changeDate/', views.changeDate, name='changeDate'),
path('MakeMyCourse/', views.MakeMyCourse, name='MakeMyCourse'),
path('editMyCourse/', views.editMyCourse, name='editMyCourse'),
path('editCourse/<int:id>/', views.editCourse, name='editCourse'),

]