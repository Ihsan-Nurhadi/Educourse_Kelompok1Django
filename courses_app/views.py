from typing import Any
from django.db.models import Q
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
    template_name = 'courses_app/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        # Ambil parameter pencarian dari URL
        search_query = self.request.GET.get('search', '')

        # Query default: hanya post yang sudah dipublikasikan
        queryset = Post.objects.filter(published_date__lte=timezone.now())

        # Jika ada parameter pencarian, filter berdasarkan title atau text
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(text__icontains=search_query)
            )

        # Urutkan berdasarkan tanggal publikasi terbaru
        return queryset.order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context
    
class ClassListView(ListView):
    model = Class
    template_name = 'courses_app/class_list.html'
    context_object_name = 'classes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mendapatkan post berdasarkan pk yang diteruskan di URL
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Menambahkan post ke dalam konteks
        context['post'] = post
        return context

    def get_queryset(self):
        # Mendapatkan post berdasarkan pk yang diteruskan
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Mengambil kelas yang terkait dengan post tersebut
        return Class.objects.filter(post=post)

class ClassDetailView(LoginRequiredMixin, DetailView):
    model = Class
    template_name = 'courses_app/class_detail.html'
    context_object_name = 'class_instance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_instance = self.object
        context['form'] = ClassForm(instance=class_instance)  # Form untuk mengedit kelas
        return context
    
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

class ClassCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = ClassForm
    model = Class
    template_name = 'courses_app/create_class.html'

    def get_form_kwargs(self):
        """
        Override method ini untuk mengirimkan user ke ClassForm.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Kirim user yang sedang login
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Tambahkan informasi tambahan ke context.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Ambil semua post yang dibuat oleh user
        context['posts'] = Post.objects.filter(author=user)
        return context

    def form_valid(self, form):
        """
        Validasi form sebelum menyimpan.
        """
        class_instance = form.save(commit=False)
        # Pastikan post milik user yang sedang login
        if class_instance.post.author != self.request.user:
            form.add_error('post', "Anda tidak memiliki izin untuk menggunakan post ini.")
            return self.form_invalid(form)
        class_instance.save()
        return redirect('user_app:teacherdashboard')  # Arahkan ke halaman post_detail setelah menyimpan kelas


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
    return redirect('user_app:teacherdashboard')

@login_required
def post_(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
