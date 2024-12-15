from django.contrib import admin
from .models import Post , Class, Lesson, Subchapter
# Register your models here.
admin.site.register(Post)
admin.site.register(Class)
admin.site.register(Lesson)
admin.site.register(Subchapter)