# cart.py
from user_app.models import Product, User
from courses_app.models import Post
from .models import Cart
import json
from decimal import Decimal
class CartHandler():  # Renaming from Cart to CartHandler
    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.user = self.request.user

        if self.user.is_authenticated:
            self.cart_items = Cart.objects.filter(user=self.user)  # This refers to the Cart model
        else:
            self.cart_items = []

    def add_student(self, post):
        post_id = post.id
        cart_item, created = Cart.objects.get_or_create(user=self.user, post=post)
        if not created:
            cart_item.quantity = 1
            cart_item.save()

    def add_teacher(self, product):
        product_id = product.id
        cart_item, created = Cart.objects.get_or_create(user=self.user, product=product)
        if not created:
            cart_item.quantity = 1
            cart_item.save()

    def delete(self, post):
        Cart.objects.filter(user=self.user, post=post).delete()
    
    def cart_total(self):
        total = Decimal('0.00')  # Initialize total as a Decimal
        for item in self.cart_items:
            if item.post:
                total += Decimal(item.post.price) * Decimal(item.quantity)  # Ensure item.price is a Decimal
            elif item.product:
                total += Decimal(item.product.sell_price) * Decimal(item.quantity)  # Ensure product.sell_price is a Decimal
        return total

    def __len__(self):
        return sum(item.quantity for item in self.cart_items)

    def get_prodss(self):
        # Get IDs from cart_items
        post_ids = [item.post.id for item in self.cart_items if item.post]  # Collect post IDs
        # Use IDs to lookup posts in the database model
        products = Post.objects.filter(id__in=post_ids)  # Query database for Posts
        return products

    def get_prods(self):
        # Get IDs from cart_items
        product_ids = [item.product.id for item in self.cart_items if item.product]  # Collect product IDs
        # Use IDs to lookup products in the database model
        products = Product.objects.filter(id__in=product_ids)  # Query database for Products
        return products