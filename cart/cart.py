from user_app.models import Product
from courses_app.models import Post
from django.contrib.sessions.models import Session


class Cart():
    def __init__(self, request):
        self.session = request.session

        #get the current session key if it exists
        cart = self.session.get('session_key')

        #if the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #make sure cart is available  on all pages of site
        self.cart = cart

    def add_teacher(self, product):
        product_id = str(product.id)

        #logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.sell_price)}

        self.session.modified = True

    def add_student(self, post):
        post_id = str(post.id)

        #logic
        if post_id in self.cart:
            pass
        else:
            self.cart[post_id] = {'price': str(post.price)}

        self.session.modified = True

    def __len__(self):
        return len(self.cart)
    

    def get_prods(self):
        #get ids from cart
        product_ids = self.cart.keys()
        #use ids to lookup product in db model
        products = Product.objects.filter(id__in=product_ids)
        #return those look up products
        return products
    
    def get_prodss(self):
        #get ids from cart
        product_ids = self.cart.keys()
        #use ids to lookup product in db model
        products = Post.objects.filter(id__in=product_ids)
        #return those look up products
        return products

