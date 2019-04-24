from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import Product, Table, Bill, Product_Image, Cover, Direction, Category, UserProfile, Wallet, Bill_detail


class product(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'img']
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
    list_display = ['creation_date', 'finished']
    list_filter = ['creation_date']
    search_fields = ['creation_date']
    ordering = ['creation_date']


class category(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']

from django.contrib.sessions.models import Session

from chat.models import Message, Conversation

admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(Session)
admin.site.register(Product, product)
admin.site.register(Direction, direction)
admin.site.register(Table, table)
admin.site.register(Product_Image, image)
admin.site.register(Cover, cover)
admin.site.register(Bill, bill)
admin.site.register(Category, category)
admin.site.register(UserProfile)
admin.site.register(Wallet)
admin.site.register(Bill_detail)
