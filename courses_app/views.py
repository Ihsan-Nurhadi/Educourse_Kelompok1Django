from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.query import QuerySet
from django.views.generic import (ListView, 
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from courses_app.models import Post , Class
from courses_app.forms import PostForm , ClassForm
from user_app.models import User  # Ganti Teacher dengan User
# Create your views here.

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ambil semua kelas terkait dengan post ini
        post = self.object
        context['classes'] = post.classes.all()  # Mengambil semua kelas terkait dengan post ini
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = PostForm
    model = Post
    template_name = 'courses_app/post_form.html'  # Pastikan Anda menentukan template yang tepat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ganti Teacher dengan User, gunakan is_teacher untuk filter
        user = User.objects.get(username=self.request.user.username)
        if user.is_teacher:
            context['posts'] = Post.objects.filter(author=user).order_by('-created_date')
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        user = User.objects.get(username=self.request.user.username)
        post.author = user  # Ganti Teacher dengan User
        post.save()
        # Setelah menyimpan post, arahkan ke halaman post_draft_list, bukan create_class
        return redirect('post_draft_list')


# views.py
class ClassCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = ClassForm
    model = Class
    template_name = 'courses_app/create_class.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Ambil semua post yang dibuat oleh teacher
        context['posts'] = Post.objects.filter(author=user)
        return context

    def form_valid(self, form):
        # Simpan kelas terkait dengan post yang dipilih
        class_instance = form.save(commit=False)
        post = form.cleaned_data['post']
        class_instance.post = post  # Kaitkan kelas dengan post yang dipilih
        class_instance.save()
        return redirect('post_detail', pk=post.pk)  # Arahkan ke halaman post_detail setelah menyimpan kelas



class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        # Simpan post terlebih dahulu
        post = form.save(commit=False)
        post.save()  # Save post ke database
        # Redirect ke halaman draft list
        return redirect('post_draft_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Post
    template_name = 'courses_app/post_draft_list.html'
    context_object_name = 'posts'  # Change default 'object_list' to 'posts'

    def get_queryset(self):
        # Get the User instance related to the logged-in User
        user = User.objects.get(username=self.request.user.username)
        if user.is_teacher:
            return Post.objects.filter(author=user, published_date__isnull=True).order_by('created_date')
        return Post.objects.none()  # Jika user bukan teacher, tidak ada post draft yang ditampilkan
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_new')

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
