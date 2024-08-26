from store.models import Product, Profile
class Cart():
    def __init__(self, request):
        self.session = request.session

        # get request
        self.request = request

        # get the current seesion if it exists
        cart = self.session.get('session_key')
        # if user new, no session key so we create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}


        # make sure cart is available on all pages
        self.cart = cart


    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '2':3} to {"3":1,"2":3}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save the carty to the profile old_cart field
            current_user.update(old_cart=str(carty))

# this function adds evrytime we add item to cart
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '2':3} to {"3":1,"2":3}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save the carty to the profile old_cart field
            current_user.update(old_cart=str(carty))


    def __len__(self):
        return len(self.cart)

    def get_products(self):
        # getting id from cart
        product_ids = self.cart.keys()
        # use the ids to lookup prods in the database model
        products = Product.objects.filter(id__in=product_ids)
        # return the looked up products
        return products


    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # get cart
        ourcart = self.cart
        # update dict
        ourcart[product_id] = product_qty

        self.session.modified - True

        # deal with logged in user
        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '2':3} to {"3":1,"2":3}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save the carty to the profile old_cart field
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing

    def cart_total(self):
        # get product ids
        product_ids = self.cart.keys()
        # lookup our keys in the product model
        products = Product.objects.filter(id__in=product_ids)
        # get quantities
        quantities = self.cart
        # start counting from 0
        total = 0
        for key, value in quantities.items():
            # convert the key into int for calc
            key = int(key)
            for product in products:
                if product.is_sale:
                    total = total + (product.sale_price * value)
                else:
                    total = total + (product.price * value)
        return total


    def delete(self, product):
        product_id = str(product)
        # delete from dictionary
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '2':3} to {"3":1,"2":3}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save the carty to the profile old_cart field
            current_user.update(old_cart=str(carty))