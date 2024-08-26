from django.shortcuts import render
from cart.cart import Cart
from payment.forms import ShippingForm
from .models import ShippingAddress
from django.contrib.auth.models import User

# Create your views here.
def checkout(request):
    cart = Cart(request)
    # getting the products from the cart
    cart_products = cart.get_products
    totals = cart.cart_total()
    quantities = cart.get_quants

    if request.user.is_authenticated:
        # checkout as user
        current_user = User.objects.get(id=request.user.id)
        # try:
        shipping_user = ShippingAddress.objects.get(user__id=current_user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {"cart_products": cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})
    else:
        # checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {"cart_products": cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})




def payment_success(request):
    return render(request, 'payment/payment_success.html', {})