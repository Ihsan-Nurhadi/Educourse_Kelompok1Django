from django.urls import path
from . import views

urlpatterns = [
    path('payment/',views.payment, name='payment'),
    path('payment_t/',views.payment_t, name='payment_t'),
    path('notification/', views.payment_notification, name='payment_notification'),
    path('finish/', views.payment_finish, name='payment_finish'),
]