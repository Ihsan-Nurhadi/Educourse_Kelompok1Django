# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from user_app.models import User, Product
from courses_app.models import Post
from .cart import CartHandler  # Update import

def cart_summary_student(request):
    cart = CartHandler(request)
    cart_products_student = cart.get_prodss()
    totals = cart.cart_total()
    return render(request, "cart_student.html", {'cart_products_student': cart_products_student, "totals": totals})

def cart_summary_teacher(request):
    cart = CartHandler(request)
    cart_products = cart.get_prods()
    totals = cart.cart_total()
    return render(request, "cart.html", {'cart_products': cart_products, 'totals': totals})

def cart_add(request):
    cart = CartHandler(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        cart.add_teacher(product=product)
        cart_quantity = len(cart)
        return JsonResponse({'qty': cart_quantity})

def cart_add_student(request):
    cart = CartHandler(request)
    if request.POST.get('action') == 'post':
        post_id = int(request.POST.get('post_id'))
        post = get_object_or_404(Post, id=post_id)
        cart.add_student(post=post)
        cart_quantity_student = len(cart)
        return JsonResponse({'qty': cart_quantity_student})

def cart_delete(request):
    cart = CartHandler(request)
    if request.POST.get('action') == 'post':
        post_id = int(request.POST.get('post_id'))
        cart.delete(post=post_id)
        return JsonResponse({'post': post_id})
    
def cart_delete_product(request):
    cart = CartHandler(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.deleteproduct(product=product_id)
        return JsonResponse({'product': product_id})