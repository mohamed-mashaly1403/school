from django.urls import path
from . import views
urlpatterns = [
    path('checkout/<str:slug>/<int:lessons>/<int:price>/<str:is_trial>', views.checkout, name='checkout'),
    path('place_order/<int:needed_course_id>/<int:price>/<int:lessons>/<str:is_trial>', views.place_order, name='place_order'),
    path('Editplaceorder/<int:order_number>/', views.Editplaceorder, name='Editplaceorder'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('order_details/<int:order_id>', views.order_details, name='order_details'),
    path('submit_review/<int:course_id>/<int:order_id>/', views.submit_review, name='submit_review'),

    path('ChangeTeacherRequest/<int:order_id>/', views.ChangeTeacherRequest, name='ChangeTeacherRequest'),

    path('complains/', views.complains, name='complains'),

]
