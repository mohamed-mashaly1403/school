from django.urls import path
from . import views
urlpatterns = [
    path('checkout/<str:slug>/<int:lessons>/<int:price>/', views.checkout, name='checkout'),
    path('place_order/<int:needed_course_id>/<int:price>/<int:lessons>/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),

    ]
