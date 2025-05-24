from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import secrets
import string
from datetime import datetime


def generate_order_id():
    prefix = "ORD"
    year = datetime.now().year
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")  # precise timestamp
    random_part = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(4))
    return f"{prefix}-{year}-{timestamp}-{random_part}"

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products', default="noimage.jpg", null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Ratings(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=0)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)


class Order(models.Model):
    products = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=15, default=generate_order_id(), editable=False, unique=False, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=150, default='pending', null=True, blank=True)
    wilaya = models.CharField(max_length=100, null=True, blank=True)
    commune = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)

class Tracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=150)
    