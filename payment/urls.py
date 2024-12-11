from django.urls import path
from . import views

urlpatterns = [
    path('payment/',views.payment, name='payment'),
    path('payment_t/',views.payment_t, name='payment_t'),
]