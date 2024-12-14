from django.urls import path
from user_app import views

app_name = 'user_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('ourteam', views.team, name='team'),
    path('student', views.student, name='student'),
    path('teacher', views.teacher, name='teacher'),
    path('faq', views.faq, name='faq'),
    path('contact', views.contact, name='contact'),    
    path('studentdashboard', views.studentdashboard, name='studentdashboard'),
    path('teacherdashboard', views.teacherdashboard, name='teacherdashboard'),
    path('teacherscourses', views.teacherscourses, name='teacherscourses'),
    path('teacherscourses/<str:slug>', views.productcourses, name='productcourses'),
    path('teacherscourses/<str:cate_slug>/<str:prod_slug>', views.productdetails, name='productdetails'),
    path('studentprofile',views.studentprofile, name='studentprofile'),
    path('teacherprofile',views.teacherprofile, name='teacherprofile'),
    path('update_studentprofile/', views.update_studentprofile, name='update_studentprofile'),
    path('update_teacherprofile/', views.update_teacherprofile, name='update_teacherprofile'),
    path('buat_iklanpromosi/', views.buat_iklanpromosi, name='buat_iklanpromosi'),
]