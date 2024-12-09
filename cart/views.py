from django.shortcuts import render, get_object_or_404
from .cart import Cart
from user_app.models import Product
from django.http import JsonResponse,  HttpResponse
# Create your views here.

def cart_summary_student (request):
    return render(request, "cart_student.html",{})

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
        cart.add(product=product)

    #     # return response
    #     response = JsonResponse({'Product Name : ': product.name })
    #     return response
    # else:
    #     return HttpResponse('This view only handles POST requests.')  # Respon untuk request lain

        #Get cart quantity
        cart_quantity = cart.__len__()

        #return response
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty: ': cart_quantity})
        return response
    
# def cart_delete(request):
#     pass

# def cart_update(request):
#     pass