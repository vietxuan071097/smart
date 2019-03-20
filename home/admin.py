from django.contrib import admin
from .models import Product, Table, Bill, Product_Image, Cover, Direction, Species


class product(admin.ModelAdmin):
    list_display = ['name', 'species', 'price']
    list_filter = ['date']
    search_fields = ['name']


class table(admin.ModelAdmin):
    list_display = ['name', 'direction', 'rfid']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']


class direction(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']


class image(admin.ModelAdmin):
    list_display = ['id', 'product', 'img']
    list_filter = ['id']
    search_fields = ['id']
    ordering = ['id']


class cover(admin.ModelAdmin):
    list_display = ['name', 'img']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['id']


class bill(admin.ModelAdmin):
    list_display = ['table', 'creation_date', 'checked_out']
    list_filter = ['table']
    search_fields = ['table']
    ordering = ['table']

class species(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']

admin.site.register(Product, product)
admin.site.register(Direction, direction)
admin.site.register(Table, table)
admin.site.register(Product_Image, image)
admin.site.register(Cover, cover)
admin.site.register(Bill, bill)
admin.site.register(Species, species)
