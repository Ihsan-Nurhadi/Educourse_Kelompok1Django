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
from courses_app.models import Post , Class, Lesson, Subchapter
from courses_app.forms import PostForm , ClassForm
from user_app.models import User  # Ganti Teacher dengan User
from payment.models import Order , OrderItem
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

    
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Ambil semua kelas terkait dengan post ini
        context['classes'] = post.classes.all()

        # Cek apakah user memiliki order terkait dengan post ini dan status True
        user = self.request.user
        if user.is_authenticated:
            context['has_active_order_for_post'] = OrderItem.objects.filter(
                order__user=user,  # User yang login
                order__status=True,  # Order dengan status True
                post=post  # Post yang sedang dilihat
            ).exists()
        else:
            context['has_active_order_for_post'] = False

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

class LessonListView(ListView):
    model = Lesson
    template_name = 'courses_app/lesson_list.html'
    context_object_name = 'lessons' 

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'courses_app/lesson_detail.html' 
    context_object_name = 'lesson' 

    # Menambahkan produk dan subchapter yang terkait ke dalam konteks
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()  # Mendapatkan objek lesson berdasarkan pk
        
        # Menambahkan produk terkait lesson ke dalam konteks
        context['products'] = lesson.products.all()  # Mengambil semua produk terkait dengan lesson
        
        # Menambahkan subchapter terkait lesson ke dalam konteks
        context['subchapters'] = Subchapter.objects.filter(Sub=lesson)  # Filter subchapter berdasarkan lesson
        return context
    
class ChapterListView(ListView):
    model = Subchapter
    template_name = 'courses_app/courses_list.html'
    context_object_name = 'subchapters'

    def get_queryset(self):
        lesson_id = self.kwargs.get('pk')  # Ambil pk dari URL, jika tersedia
        if lesson_id:
            return Subchapter.objects.filter(Sub__id=lesson_id)
        return Subchapter.objects.all()  # Default: semua subchapter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tambahkan data Lessons terkait ke dalam konteks
        context['lessons'] = Lesson.objects.filter(chapters__in=context['subchapters']).distinct()
        return context

class ChapterDetailView(DetailView):
    model = Subchapter
    template_name = 'courses_app/courses_detail.html' 
    context_object_name = 'subchapter' 

     # Menambahkan produk yang terkait dengan kelas ini ke dalam konteks
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subchapter = self.get_object()  # Mendapatkan objek lesson berdasarkan pk

        # Menambahkan produk terkait kelas ini ke dalam konteks
        context['Sub'] = subchapter.Sub.all()  # Mengambil semua produk terkait dengan lesson
        return context