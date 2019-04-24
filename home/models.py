from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Cover(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True)
    detail = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return self.name


class Product_Image(models.Model):
    img = models.ImageField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Direction(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Table(models.Model):
    name = models.CharField(max_length=100)
    direction = models.ForeignKey(Direction, null=True, on_delete=models.CASCADE)
    rfid = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return self.name


class Bill(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    order_method = models.BooleanField(default=False)
    table = models.ForeignKey(Table, null=True, on_delete=models.CASCADE)
    address = models.CharField(blank=True, null=True, max_length=200)
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    creation_date = models.DateTimeField(null=True)
    paid = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    def get_date(self):
        return self.creation_date

    def __str__(self):
        return str(self.id)


class Bill_detail(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def total_price(self):
        return self.quantity * self.product.price


class Sex(models.Model):
    name = models.CharField(max_length=10)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    birthday = models.DateField(null=True)
    sex = models.ForeignKey(Sex, null=True, on_delete=models.CASCADE)
    img = models.ImageField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.user.username)


class Wallet(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    point = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username)
