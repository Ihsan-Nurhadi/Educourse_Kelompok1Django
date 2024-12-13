from django.shortcuts import render
from cart.cart import CartHandler

# Create your views here.
def payment(request):
    cart = CartHandler(request)
    cart_products_student = cart.get_prodss
    totals = cart.cart_total()
    return render(request,"payment/payment.html",{'cart_products_student':cart_products_student,"totals":totals}) 

def payment_t(request):
    cart = CartHandler(request)
    cart_products = cart.get_prods
    totals = cart.cart_total()
    return render(request,"payment/payment_.html",{'cart_products':cart_products,"totals":totals}) 