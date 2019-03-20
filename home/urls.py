from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('cart/', views.cart, name='cart'),
    path('success/', views.success, name='success'),
    path('detail/<int:product_id>', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('remove/', views.remove, name='remove'),
    path('logout/', auth_views.LogoutView.as_view(next_page="/"), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name="home/login.html"), name='login'),
    path('register/', views.register, name='register'),
    path('add-product/', views.add_product, name='add_product'),
]
