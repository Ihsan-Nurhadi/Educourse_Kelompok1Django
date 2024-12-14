from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/classes/', views.ClassListView.as_view(), name='class_list'),
    path('class/<int:pk>/', views.ClassDetailView.as_view(), name='class_detail'),  # URL untuk ClassDetailView
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('drafts/', views.DraftListView.as_view(), name='post_draft_list'),
    path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
    path('create_class/', views.ClassCreateView.as_view(), name='create_class'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('lesson_list', views.LessonListView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]