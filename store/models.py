from django.db import models
import datetime

# for extending the profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save #this helps to update the user profile for every user that is created.

# create the customer profile
class Profile(models.Model):
    # associate model with User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=15, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=15, blank=True)
    zipcode = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=15, blank=True)
    # this line below is to turn the cart dictionary into a string so that we are able to store it in the database
    old_cart = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return self.user.username

# create the user profile
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# automating the profile thing
post_save.connect(create_profile, sender=User)


# Create your models here.
# these are the categories
class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='assets/cover', default='default.jpg')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


# customers
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# all products
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=2500, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    # Add the sale token
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.name


# orders
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product}'