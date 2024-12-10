from django.shortcuts import render, get_object_or_404
from .cart import Cart
from user_app.models import Product
from courses_app.models import Post
from django.http import JsonResponse
# Create your views here.

# student
def cart_summary_student (request):
    cart = Cart(request)
    cart_products_student = cart.get_prodss
    return render(request, "cart_student.html",{'cart_products_student':cart_products_student})

# teacher
def cart_summary_teacher (request):
    cart = Cart(request)
    cart_products = cart.get_prods
    return render(request, "cart.html", {'cart_products':cart_products})

# tutorial pertama
def cart_add(request):
    # Get the cart
    cart = Cart(request)
    #test for post
    if request.POST.get('action') == 'post':
        #get stuff 
        product_id = int(request.POST.get('product_id'))
        #lookup product in DB
        product = get_object_or_404(Product, id=product_id)
        #save to session
        cart.add_teacher(product=product)

        #Get cart quantity
        cart_quantity = cart.__len__()

        #return response
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty: ': cart_quantity})
        return response

def cart_add_student(request):
    # Get the cart
    cart = Cart(request)
    #test for post
    if request.POST.get('action') == 'post':
        #get stuff 
        post_id = int(request.POST.get('post_id'))
        #lookup post in DB
        post = get_object_or_404(Post, id=post_id)
        #save to session
        cart.add_student(post=post)

        #Get cart quantity
        cart_quantity_student = cart.__len__()

        #return response
        # response = JsonResponse({'Post title: ': post.title})
        response = JsonResponse({'qty: ': cart_quantity_student})
        return response

# def cart_delete(request):
#     pass

# def cart_update(request):
#     pass