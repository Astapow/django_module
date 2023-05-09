from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    wallet = models.DecimalField(decimal_places=2, max_digits=20)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    img = models.ImageField(upload_to='static/images/', blank=True, null=True)
    stock_availability = models.PositiveIntegerField()

    def __str__(self):
        return f'Name: {self.name} Description: {self.description} ' \
               f'Price: {self.price} Stock availability: {self.stock_availability}'


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    buy_at = models.DateTimeField(auto_now=True)


class Return(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)
