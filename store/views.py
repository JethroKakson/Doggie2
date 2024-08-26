from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout #for enabling the authentication process.
from django.contrib import messages # for feedback
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, PasswordForm, UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.core.exceptions import ObjectDoesNotExist


def search(request):
    # determiine if they filled the form
    if request.method == "POST":
        searched = request.POST['searched']
        # query the product database
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched)) #icontains makes the search not to be case sensitive
        # test for null
        if not searched:
            messages.success(request, "Sorry, this product does not exist")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})

def update_info(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        # try:
        shipping_user = ShippingAddress.objects.get(user__id=current_user.id)
        # except ShippingAddress.DoesNotExist:
            # shipping_user = None
        # current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        # try:
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        # except ShippingAddress.DoesNotExist:
            # shipping_user = None

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            # login(request, current_user)
            messages.success(request, "User Info has been updated!!")
            return redirect('home')
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.success(request, "You must be logged in!")
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            form = PasswordForm(user, request.POST)
            # is the form vcalid?
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set successfully")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = PasswordForm(user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')
    # return render(request, 'update_password.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = UpdateUserForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, "User has been updated!!")
            return redirect('home')
        return render(request, 'update_user.html', {'form': form})
    else:
        messages.success(request, "You must be logged in!")
        return redirect('home')

    # return render(request, 'update_user.html', {'form': form})


# Create your views here.
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # the shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # get the saved cart from old_cart
            saved_cart = current_user.old_cart
            # convert the db to python dictionary
            if saved_cart:
                # convert to dict using json
                converted_cart = json.loads(saved_cart)
                # add the loaded dict to the session
                # get the cart
                cart = Cart(request)
                # loop thru the cart and add the items to the db
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ('You have been logged in'))
            return redirect('home')
        else:
            messages.error(request, ('There was an error logging in, try again'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out, Hope to see you soon."))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ('You have been registered, you can now login and logout'))
            return redirect('home')
        else:
            messages.success(request, ('There was an error during account registration, try agin'))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})


def category(request, name):
    # replacing - for ' '
    name = name.replace('-', ' ')
#     checking for the category from the url
    try:
    #     look up the category
        category = Category.objects.get(name=name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.error(request, 'That category does not exist!!')
        return redirect('home')