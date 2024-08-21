from django.shortcuts import render, get_object_or_404
from .cart import Cart
from django.contrib import messages
from store.models import Product
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    # get the cart
    cart = Cart(request)
    # getting the products from the cart
    cart_products = cart.get_products
    totals = cart.cart_total()
    quantities = cart.get_quants
    return render(request, 'cart_summary.html', {"cart_products": cart_products, 'quantities': quantities, 'totals': totals})


def cart_add(request):
#     getting cart
    cart = Cart(request)
# test the POST
    if request.POST.get('action') == 'post': # this is because in ajax we used the lowercase post for the action
#         get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
#         lookup product in database
        product = get_object_or_404(Product, id=product_id)
#     save to session
        cart.add(product=product, quantity=product_qty)

# Get cart quantity
        cart_quantity = cart.__len__()

#         return response
#         response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty: ': cart_quantity})
        messages.success(request, ("Product has been added to cart."))
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':  # this is because in ajax we used the lowercase post for the action
        #         get stuff
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request, ("Product has been deleted successfully."))
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':  # this is because in ajax we used the lowercase post for the action
        #         get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = str(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty': product_qty})
        messages.success(request, ("Product has been updated successfully."))
        return response


