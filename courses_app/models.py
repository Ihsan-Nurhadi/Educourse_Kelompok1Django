# Create your models here.
# courses_app.models
from django.db import models
from django.utils import timezone
from django.urls import reverse
from embed_video.fields import EmbedVideoField
from user_app.models import User, Product  # Import User dari user_app

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Ganti Teacher menjadi User
    title = models.CharField(max_length=200)
    text = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_date = models.DateTimeField(default=timezone.now)
    thumbnail = models.ImageField(upload_to='thumbnail', blank=True)
    video = EmbedVideoField(blank=True, null=True)  # Tambahkan field untuk video
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    # Method untuk cek apakah author adalah seorang guru
    def is_teacher(self):
        return self.author.is_teacher

class Class(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='classes')  # Relasi dengan Post
    class_name = models.CharField(max_length=100)
    text = models.TextField()
    video = EmbedVideoField(blank=True, null=True)

    def __str__(self):
        return self.class_name
    

class Lesson(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Ganti Teacher menjadi User
    products = models.ManyToManyField(Product, related_name='lessons')  # ManyToManyField ke Product
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    thumbnail = models.ImageField(upload_to='thumbnail', blank=True)
    video = EmbedVideoField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('lesson_detail', kwargs={'pk': self.pk})

    # def __str__(self):
        # return self.author

    # Method untuk cek apakah author adalah seorang guru
    def is_teacher(self):
        return self.author.is_teacher
    
class Subchapter(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Ganti Teacher menjadi User
    course_name = models.CharField(max_length=255)
    text = models.TextField()
    Sub = models.ManyToManyField(Lesson, related_name='chapters')
    video = EmbedVideoField(blank=True, null=True)

    def __str__(self):
        return self.course_name