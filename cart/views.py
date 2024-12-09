from django.shortcuts import render, get_object_or_404
from .cart import Cart
from user_app.models import Product
from django.http import JsonResponse
# Create your views here.

#tutorial 3

def cartPage (request):
    return render(request, "cart.html")

# def cartPage (request):
#     cart = Cart(request)
#     cart_products = cart.get_prods
#     return render(request, "cart.html", {'cart_products':cart_products})

# tutorial pertama
# def cart_add(request):
#     # Get the cart
#     cart = Cart(request)
#     #test for post
#     if request.POST.get('action') == 'post':
#         #get stuff
#         product_id = int(request.POST.get('product_id'))
#         #lookup product in DB
#         product = get_object_or_404(Product, id=product_id)
#         #save to session
#         cart.add(product=product)

#         #tutorial 2
#         #Get cart quantity
#         cart_quantity = cart.__len__()

#         #return response
#         # response = JsonResponse({'Product Name: ': product.name})
#         #tutorial 2
#         response = JsonResponse({'qty: ': cart_quantity})
#         return response
    
# def cart_delete(request):
#     pass

# def cart_update(request):
#     pass