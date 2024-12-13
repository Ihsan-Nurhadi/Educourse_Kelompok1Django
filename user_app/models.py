from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime
import os

# Create your models here.
class User(AbstractUser):
    is_teacher= models.BooleanField('Is teacher', default=False)
    is_student = models.BooleanField('Is student', default=False)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

def get_file_path(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/', filename)

class Category(models.Model):
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    desc = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    small_desc = models.CharField(max_length=250, null=False, blank=False)
    desc = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    ori_price = models.FloatField(null=False,blank=False)
    sell_price = models.FloatField(null=False,blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=10, primary_key=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Generate ID hanya saat membuat objek baru
            last_product = Product.objects.order_by('-id').first()
            if last_product:
                self.id = f"PROD{int(last_product.id[4:]) + 1:03d}"
            else:
                self.id = "PROD001"
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

class Contact(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
