from .cart import Cart


# update sinkron database Cart
def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        print(f"Context Processor Cart Items: {cart_items.values()}")  # Debugging
        return {'cart': cart_items}
    return {'cart':[]}