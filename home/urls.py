from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-product/', views.add_product, name='add-product'),
    path('cart/', views.cart, name='cart'),
    path('pay/', views.pay, name='pay'),
    path('success/', views.success, name='success'),
    path('new-bill/', views.new_bill, name='new-bill'),
    path('detail/<int:product_id>', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('remove/', views.remove, name='remove'),
    path('logout/', auth_views.LogoutView.as_view(next_page="/"), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name="home/login.html"), name='login'),
    path('register/', views.register, name='register'),
    path('new-product/', views.new_product, name='new-product'),
    path('profile/', views.profile, name='profile'),
    path('bill-detail/<int:id>', views.bill_detail, name='bill-detail'),
    path('finish/<int:id>', views.finish, name = 'finish'),
]
