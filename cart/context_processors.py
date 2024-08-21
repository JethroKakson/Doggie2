from .cart import Cart

# create our context processor so that our cart can work on all pages.
def cart(request):
    # return data from our cart
    return {'cart': Cart(request)}