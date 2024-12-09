from django.urls import path
from . import views

urlpatterns = [
    path('student/',views.cart_summary_student, name='cart_summary_student'),
    path('teacher/',views.cart_summary_teacher, name='cart_summary_teacher'),
    path('add/',views.cart_add, name='cart_add'),
    # path('delete/',views.cart_delete, name='cart_delete'),
    # path('update/',views.cart_update, name='cart_update'),
]