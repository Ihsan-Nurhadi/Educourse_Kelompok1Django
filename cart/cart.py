from user_app.models import Product, User
from courses_app.models import Post
from django.contrib.sessions.models import Session
import json

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # If the user is authenticated, load the cart from their saved data
        if self.request.user.is_authenticated:
            current_user = User.objects.filter(id=self.request.user.id).first()
            if current_user and current_user.old_cart:
                # Load old_cart from user and update session
                old_cart = json.loads(current_user.old_cart)
                cart.update(old_cart)

        self.cart = cart

    def add_student(self, post):
        post_id = str(post.id)

        # Logic
        if post_id in self.cart:
            pass
        else:
            self.cart[post_id] = {'price': str(post.price)}

        self.session.modified = True

        # Save cart to User model if logged in
        if self.request.user.is_authenticated:
            self.save_cart_to_user()

    def save_cart_to_user(self):
        """Save the current cart to the User model."""
        if self.request.user.is_authenticated:
            current_user = User.objects.filter(id=self.request.user.id).first()
            if current_user:
                carty = json.dumps(self.cart)  # Convert cart to JSON
                current_user.old_cart = carty
                current_user.save()

    def add_teacher(self, product):
        product_id = str(product.id)

        # Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.sell_price)}

        self.session.modified = True

        # Save cart to User model if logged in
        if self.request.user.is_authenticated:
            self.save_cart_to_user()

    def delete(self, post):
        post_id = str(post.id)
        if post_id in self.cart:
            del self.cart[post_id]

        self.session.modified = True

        # Save cart to User model if logged in
        if self.request.user.is_authenticated:
            self.save_cart_to_user()

    def cart_total(self):
        product_ids = self.cart.keys()
        products = Post.objects.filter(id__in=product_ids)
        # Start counting at 0
        total = 0

        for product in products:
            total += float(self.cart[str(product.id)]['price'])

        return total

    def __len__(self):
        return len(self.cart)

    def get_prodss(self):
        # Get IDs from cart
        product_ids = self.cart.keys()
        # Use IDs to lookup posts in database model
        products = Post.objects.filter(id__in=product_ids)
        # Return those looked-up posts
        return products
    
    def get_prods(self):
        # Get IDs from cart
        product_ids = self.cart.keys()
        # Use IDs to lookup posts in database model
        products = Product.objects.filter(id__in=product_ids)
        # Return those looked-up posts
        return products