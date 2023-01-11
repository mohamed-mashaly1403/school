from django.urls import path, include
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path("homeg/", views.homeg, name='homeg'),
    path('login/', views.login, name='login'),
    # path('glogin/', views.glogin, name='glogin'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('resetPassordPage/', views.resetPassordPage, name='resetPassordPage'),
    path('change_password/', views.change_password, name='change_password'),
    path('resetPasswordValidate/<uidb64>/<token>/', views.resetPasswordValidate, name='resetPasswordValidate'),
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('myOrders/', views.myOrders, name='myOrders'),
    path('myActiveOrders/', views.myActiveOrders, name='myActiveOrders'),
    path('UnPaidOrders/', views.UnPaidOrders, name='UnPaidOrders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('deltePhoto', views.deltePhoto, name='deltePhoto'),
    path('inbox/', views.inbox, name="inbox"),
    path('viewMessage/<str:pk>/', views.viewMessage, name="viewMessage"),
    path('reply/<str:pk>/', views.reply, name="reply"),
    path('DeleteMessage/<str:pk>/', views.DeleteMessage, name="DeleteMessage"),
    path('DeleteMessages/', views.DeleteMessages, name="DeleteMessages"),
    path('createMessage/<str:pk>/', views.createMessage, name="createMessage"),
    path('createMessagefromStudent/<str:pk>/', views.createMessagefromStudent, name="createMessagefromStudent"),
    path('social-auth/', include('social_django.urls', namespace='social')),






]