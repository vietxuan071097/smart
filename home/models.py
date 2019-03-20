from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Cover(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(blank=True, null=True)


class Species(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    detail = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return self.name

    def number(self):
        return "{:,}".format(self.price)

    def get_img(self):
        return Product_Image.objects.filter(product=self)[0]

    def get_img_all(self):
        return Product_Image.objects.filter(product=self)


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
    table = models.ForeignKey(Table, null=True, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(null=True)
    checked_out = models.BooleanField(default=False)

    def getdate(self):
        return self.creation_date

    def getout(self):
        return self.checked_out

    def __str__(self):
        return str(self.id)


class Bill_detail(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def total_price(self):
        return self.quantity * self.product.price